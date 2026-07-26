"""
Hardware Detector
=================
Automatically detects CPU cores, RAM, and GPU (NVIDIA / AMD / Apple Silicon)
at application startup and exposes the results to the rest of the system.

Used by:
  * GPT2Backend — selects the best torch device (cuda / mps / cpu)
  * api/main.py — logs hardware summary on startup
  * BackgroundTrainer — adjusts parallelism based on core count

Detection logic
---------------
1. CPU: ``os.cpu_count()`` and ``/proc/cpuinfo``
2. RAM: ``/proc/meminfo`` (Linux) or ``ctypes.windll`` (Windows fallback)
3. GPU:
   a. NVIDIA — ``import torch; torch.cuda.is_available()``
      Falls back to parsing ``nvidia-smi`` output if torch is not yet imported.
   b. Apple Silicon — ``torch.backends.mps.is_available()``
   c. No GPU → device = "cpu"

All detection is **side-effect-free and import-safe**: heavy imports (torch)
are done lazily so the module can be imported before PyTorch is installed.
"""

from __future__ import annotations

import logging
import os
import platform
import subprocess
from dataclasses import dataclass, field
from functools import lru_cache

logger = logging.getLogger("new-mir.hw_detector")

# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class HardwareInfo:
    """Snapshot of the detected hardware capabilities."""

    # CPU
    cpu_cores: int = 1
    cpu_model: str = "Unknown"

    # RAM
    ram_total_mb: int = 0
    ram_available_mb: int = 0

    # GPU
    gpu_available: bool = False
    gpu_device: str = "cpu"          # "cuda", "cuda:0", "mps", or "cpu"
    gpu_name: str = ""               # e.g. "NVIDIA GeForce RTX 3090"
    gpu_vram_mb: int = 0             # 0 if unknown / no GPU
    gpu_count: int = 0               # number of CUDA devices

    # Computed recommendations
    recommended_workers: int = 2     # uvicorn worker processes
    recommended_torch_dtype: str = "float32"  # "float16" on capable GPUs

    # Warnings collected during detection
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "cpu_cores": self.cpu_cores,
            "cpu_model": self.cpu_model,
            "ram_total_mb": self.ram_total_mb,
            "ram_available_mb": self.ram_available_mb,
            "gpu_available": self.gpu_available,
            "gpu_device": self.gpu_device,
            "gpu_name": self.gpu_name,
            "gpu_vram_mb": self.gpu_vram_mb,
            "gpu_count": self.gpu_count,
            "recommended_workers": self.recommended_workers,
            "recommended_torch_dtype": self.recommended_torch_dtype,
            "warnings": self.warnings,
        }

    def summary(self) -> str:
        """One-line human-readable summary."""
        gpu_part = (
            f"GPU={self.gpu_name} ({self.gpu_vram_mb} MB VRAM, {self.gpu_device})"
            if self.gpu_available
            else "GPU=none (CPU only)"
        )
        return (
            f"CPU={self.cpu_cores} cores [{self.cpu_model[:40]}] | "
            f"RAM={self.ram_total_mb} MB | {gpu_part}"
        )


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------


def _detect_cpu() -> tuple[int, str]:
    """Return (core_count, model_name)."""
    cores = os.cpu_count() or 1

    model = platform.processor() or "Unknown"
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as fh:
            for line in fh:
                if "model name" in line:
                    model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass

    return cores, model[:80]


def _detect_ram() -> tuple[int, int]:
    """Return (total_mb, available_mb)."""
    total_mb = avail_mb = 0
    try:
        with open("/proc/meminfo", encoding="utf-8") as fh:
            mem: dict[str, int] = {}
            for line in fh:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(":")] = int(parts[1])
        total_mb = mem.get("MemTotal", 0) // 1024
        avail_mb = mem.get("MemAvailable", 0) // 1024
    except OSError:
        pass
    return total_mb, avail_mb


def _detect_gpu_via_torch() -> tuple[bool, str, str, int, int]:
    """
    Return (available, device_str, gpu_name, vram_mb, gpu_count) using torch.

    Only called once torch is importable.  Never raises — returns CPU defaults.
    """
    try:
        import torch  # type: ignore[import-untyped]

        # ── NVIDIA CUDA ─────────────────────────────────────────────────────
        if torch.cuda.is_available():
            count = torch.cuda.device_count()
            device = "cuda" if count == 1 else "cuda:0"
            name = torch.cuda.get_device_name(0)
            try:
                props = torch.cuda.get_device_properties(0)
                vram_mb = props.total_memory // (1024 * 1024)
            except Exception:  # noqa: BLE001
                vram_mb = 0
            return True, device, name, vram_mb, count

        # ── Apple MPS ───────────────────────────────────────────────────────
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return True, "mps", "Apple Silicon GPU", 0, 1

    except Exception:  # noqa: BLE001
        pass

    return False, "cpu", "", 0, 0


def _detect_gpu_via_smi() -> tuple[bool, str, int]:
    """
    Fallback: parse ``nvidia-smi`` output when torch is not available yet.
    Returns (available, gpu_name, vram_mb).
    """
    try:
        out = subprocess.check_output(
            ["nvidia-smi",
             "--query-gpu=name,memory.total",
             "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).decode().strip()
        if out:
            parts = [p.strip() for p in out.splitlines()[0].split(",")]
            name = parts[0] if parts else "NVIDIA GPU"
            vram_mb = int(parts[1]) if len(parts) > 1 else 0
            return True, name, vram_mb
    except Exception:  # noqa: BLE001
        pass
    return False, "", 0


# ---------------------------------------------------------------------------
# Main detection entry point
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def detect() -> HardwareInfo:
    """
    Detect all hardware and return a cached :class:`HardwareInfo`.

    Cached with ``lru_cache`` so subsequent calls are instant.
    Call ``detect.cache_clear()`` to force re-detection (e.g. after hot-plug).
    """
    hw = HardwareInfo()

    # ── CPU ─────────────────────────────────────────────────────────────────
    hw.cpu_cores, hw.cpu_model = _detect_cpu()

    # ── RAM ─────────────────────────────────────────────────────────────────
    hw.ram_total_mb, hw.ram_available_mb = _detect_ram()

    # ── GPU (torch first, smi fallback) ─────────────────────────────────────
    gpu_ok, device, name, vram_mb, count = _detect_gpu_via_torch()

    if not gpu_ok:
        # torch not yet loaded — try nvidia-smi
        smi_ok, smi_name, smi_vram = _detect_gpu_via_smi()
        if smi_ok:
            # GPU exists but torch/CUDA not configured yet
            hw.warnings.append(
                f"NVIDIA GPU '{smi_name}' detected via nvidia-smi but "
                "torch.cuda.is_available() returned False. "
                "Install nvidia-docker2 / CUDA toolkit for GPU acceleration."
            )
            # Still log the GPU but keep device=cpu for now
            hw.gpu_available = False
            hw.gpu_device = "cpu"
            hw.gpu_name = smi_name
            hw.gpu_vram_mb = smi_vram
            hw.gpu_count = 1
        # No GPU
    else:
        hw.gpu_available = True
        hw.gpu_device = device
        hw.gpu_name = name
        hw.gpu_vram_mb = vram_mb
        hw.gpu_count = count

    # ── Recommendations ──────────────────────────────────────────────────────
    # Workers: use all CPU cores but cap at 4 (more workers = more RAM used)
    hw.recommended_workers = max(1, min(hw.cpu_cores, 4))

    # torch dtype: use float16 on GPU with ≥4 GB VRAM (halves memory usage)
    if hw.gpu_available and hw.gpu_vram_mb >= 4096:
        hw.recommended_torch_dtype = "float16"
    else:
        hw.recommended_torch_dtype = "float32"

    logger.info("Hardware detected: %s", hw.summary())
    for w in hw.warnings:
        logger.warning("HW warning: %s", w)

    return hw

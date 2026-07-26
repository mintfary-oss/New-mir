"""
Knowledge Distillation: GPT-2 → NeuralCodeGen
==============================================
Uses GPT-2 (teacher, 117 M params) to generate high-quality training
examples, then fine-tunes NeuralCodeGen (student, ~5 M params) on them.

The technique is called *teacher-student training* or *knowledge distillation*:
  1. Give the teacher a seed prompt.
  2. The teacher generates a coherent continuation.
  3. The full text (prompt + continuation) becomes a training example.
  4. The student is fine-tuned on that example (standard back-prop).

The student will never match the teacher in absolute quality, but it
absorbs vocabulary patterns, reasoning structures, and factual knowledge
from the generated text, which measurably improves its own output.

Usage (from api/main.py)
------------------------
    from core.distillation import run_distillation, DEFAULT_DISTILL_PROMPTS

    result = run_distillation(teacher=_gpt2_gen, student=_neural_gen)
    print(result.to_dict())

Or via the REST API:

    POST /api/distill
    {prompts: [...], max_new_tokens: 128, temperature: 0.7, epochs: 3}
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.gpt2_backend import GPT2Backend
    from core.neural_core import NeuralCodeGen

logger = logging.getLogger("new-mir.distillation")

# ---------------------------------------------------------------------------
# Default seed prompts (one per knowledge domain from the seed data)
# ---------------------------------------------------------------------------

DEFAULT_DISTILL_PROMPTS: list[str] = [
    # Machine code & assembly
    "Machine code is the lowest level of programming. A CPU executes binary instructions encoded as bytes.",
    "Assembly language uses human-readable mnemonics like MOV, ADD, SUB, JMP that map one-to-one to machine code.",
    "In x86-64 assembly the general-purpose registers are RAX, RBX, RCX, RDX, RSI, RDI, RSP and RBP.",
    "The CALL instruction pushes the return address onto the stack and jumps to the subroutine.",
    "An ELF binary consists of a header, program headers, section headers, and the actual code and data sections.",
    # CPU architecture
    "A classic five-stage CPU pipeline consists of Fetch, Decode, Execute, Memory access, and Write-back stages.",
    "Out-of-order execution allows a modern CPU to execute instructions that are ready before earlier stalled ones.",
    "Branch prediction guesses the outcome of conditional jumps to keep the pipeline full and avoid stalls.",
    "The MESI cache coherence protocol defines four states: Modified, Exclusive, Shared, and Invalid.",
    "Hyper-Threading lets one physical CPU core appear as two logical cores by sharing execution units.",
    # Memory systems
    "The memory hierarchy from fastest to slowest: CPU registers, L1 cache, L2 cache, L3 cache, DRAM, NVMe SSD.",
    "A cache miss at L1 costs around 4 cycles; an L3 miss that goes to DRAM costs around 200 cycles.",
    "Virtual memory maps each process's virtual addresses to physical pages using a multi-level page table.",
    "The Translation Lookaside Buffer (TLB) caches recent virtual-to-physical address translations.",
    "DDR5 RAM operates at up to 6400 MT/s per channel, doubles the internal banks, and reduces power consumption.",
    # Computer components
    "A GPU contains thousands of small shader cores optimized for parallel floating-point computation.",
    "CUDA cores perform single-precision floating-point operations; Tensor Cores accelerate matrix multiplications.",
    "NVMe SSDs connect via PCIe 4.0 and achieve sequential read speeds exceeding 7000 MB/s.",
    "A motherboard's VRM (Voltage Regulator Module) converts the 12 V ATX supply into the CPU core voltage.",
    "PCIe 5.0 doubles the bandwidth of PCIe 4.0, providing 32 GT/s per lane and 128 GB/s for x16 slots.",
    # Neural networks & transformers
    "A transformer model uses self-attention to compute a weighted sum of all token representations.",
    "Backpropagation computes gradients by applying the chain rule layer by layer from output to input.",
    "The Adam optimizer adapts per-parameter learning rates using exponential moving averages of gradients.",
    "Rotary Position Embeddings (RoPE) encode position by rotating the query and key vectors in attention.",
    "SwiGLU activation combines a Swish gate with a linear projection: output = Swish(xW) ⊙ (xV).",
    # Servers & data centres
    "A server rack unit (U) is 1.75 inches tall; a standard 42U rack houses up to 42 1U servers.",
    "NUMA (Non-Uniform Memory Access) systems have multiple memory banks; accessing remote banks is slower.",
    "RAID 6 uses two distributed parity blocks, tolerating two simultaneous drive failures without data loss.",
    "10 GbE NICs are standard in modern servers; 100 GbE InfiniBand is used for high-performance computing.",
    "Docker containers share the host kernel, providing process isolation without full virtualisation overhead.",
]


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class DistillationResult:
    """Summary of one distillation run."""

    prompts_used: int = 0
    examples_generated: int = 0
    fine_tune_losses: list[float] = field(default_factory=list)
    duration_s: float = 0.0
    errors: list[str] = field(default_factory=list)

    @property
    def avg_loss(self) -> float | None:
        """Average fine-tune loss across all examples, or None if no examples."""
        if not self.fine_tune_losses:
            return None
        return sum(self.fine_tune_losses) / len(self.fine_tune_losses)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompts_used": self.prompts_used,
            "examples_generated": self.examples_generated,
            "avg_loss": (
                round(self.avg_loss, 5) if self.avg_loss is not None else None
            ),
            "duration_s": round(self.duration_s, 2),
            "errors": self.errors,
        }


# ---------------------------------------------------------------------------
# Main distillation function
# ---------------------------------------------------------------------------


def run_distillation(
    teacher: "GPT2Backend",
    student: "NeuralCodeGen",
    prompts: list[str] | None = None,
    *,
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    epochs: int = 3,
) -> DistillationResult:
    """
    Distill knowledge from *teacher* (GPT-2) into *student* (NeuralCodeGen).

    For each prompt in *prompts* (defaults to :data:`DEFAULT_DISTILL_PROMPTS`):

    1. GPT-2 generates a text continuation (*max_new_tokens* tokens).
    2. The full text ``prompt + continuation`` becomes one training example.
    3. NeuralCodeGen is fine-tuned on that example for *epochs* passes.

    Parameters
    ----------
    teacher : GPT2Backend
        A loaded GPT-2 model.  If not loaded the function returns immediately
        with an error in ``DistillationResult.errors``.
    student : NeuralCodeGen
        The nano model to be updated.  Must have weights loaded.
    prompts : list[str] | None
        Seed prompts.  Falls back to :data:`DEFAULT_DISTILL_PROMPTS`.
    max_new_tokens : int
        Maximum tokens GPT-2 generates per prompt (default 128).
        Lower values are faster; higher values transfer more context.
    temperature : float
        GPT-2 sampling temperature.  0.7 gives focused but not repetitive output.
    epochs : int
        Fine-tuning epochs per example on the student (default 3).

    Returns
    -------
    DistillationResult
        Statistics for the run.  Check ``.errors`` for any per-prompt failures.
    """
    result = DistillationResult()
    t0 = time.monotonic()

    # Guard: teacher must be loaded
    if teacher.weights is None:
        result.errors.append(
            "GPT-2 teacher not loaded — call load_demo_weights() first"
        )
        logger.warning("Distillation skipped: GPT-2 not loaded")
        result.duration_s = time.monotonic() - t0
        return result

    # Guard: student must be loaded
    if student.weights is None:
        result.errors.append(
            "NeuralCodeGen student not loaded — call load_demo_weights() first"
        )
        logger.warning("Distillation skipped: NeuralCodeGen not loaded")
        result.duration_s = time.monotonic() - t0
        return result

    used_prompts = prompts if prompts is not None else DEFAULT_DISTILL_PROMPTS
    result.prompts_used = len(used_prompts)

    logger.info(
        "Starting GPT-2 → NeuralCodeGen distillation: %d prompts, "
        "max_new_tokens=%d, temperature=%.2f, epochs=%d",
        result.prompts_used,
        max_new_tokens,
        temperature,
        epochs,
    )

    for i, prompt in enumerate(used_prompts, 1):
        try:
            # --- Step 1: generate example with GPT-2 teacher ---
            generated: str = teacher.generate(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_k=40,
                stop_sequences=["\n\n\n"],
            )
            example_text = generated.strip()
            if not example_text:
                logger.debug("Prompt %d produced empty text — skipping", i)
                continue

            result.examples_generated += 1

            # --- Step 2: fine-tune student on the generated example ---
            losses = student.fine_tune_on_examples(
                [example_text],
                epochs=epochs,
                throttle_ms=0,
            )
            result.fine_tune_losses.extend(losses)

            if i % 5 == 0:
                logger.info(
                    "Distillation progress: %d/%d prompts, avg_loss=%.4f",
                    i,
                    result.prompts_used,
                    result.avg_loss or 0.0,
                )

        except Exception as exc:  # noqa: BLE001
            short_prompt = prompt[:50]
            msg = f"Prompt {i} ('{short_prompt}…'): {exc}"
            logger.warning("Distillation error — %s", msg)
            result.errors.append(msg)

    result.duration_s = time.monotonic() - t0
    logger.info(
        "Distillation complete: %d/%d examples OK, avg_loss=%.4f, %.1fs",
        result.examples_generated,
        result.prompts_used,
        result.avg_loss or 0.0,
        result.duration_s,
    )
    return result

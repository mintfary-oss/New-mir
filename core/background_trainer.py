"""
Background Distillation Scheduler
==================================
Continuously distills knowledge from GPT-2 (teacher) into NeuralCodeGen
(student) while the server is running, using a **replay buffer** to prevent
catastrophic forgetting.

How it works
------------
Every ``interval_seconds`` (default 1800 = 30 min) a background thread:

1. Asks GPT-2 to generate ``new_per_cycle`` new examples from a rotating
   pool of seed prompts.
2. Samples ``replay_per_cycle`` examples from the replay buffer (examples
   generated in *previous* cycles).
3. Fine-tunes NeuralCodeGen on the combined batch (new + replay) so it
   never forgets what it learnt earlier.
4. Adds the newly generated texts to the replay buffer (capped at
   ``max_buffer_size`` entries — oldest entries are dropped when full).
5. Saves weights to disk atomically so the progress survives restarts.

Why replay buffer prevents forgetting
--------------------------------------
Without replay, training on cycle N overwrites knowledge from cycle N-1.
Mixing old examples into every cycle means the model sees a representative
sample of everything it has ever learnt, not just the most recent batch.
This is the same technique used in DeepMind's DQN and continual-learning
research to combat catastrophic interference.

Thread safety
-------------
All state is protected by a threading.Lock.  The HTTP handlers that also
call ``NeuralCodeGen.fine_tune_on_examples`` do *not* hold this lock, so
there can be a brief interleave, but numpy in-place updates are GIL-bound
and the lock around the scheduler's own cycle prevents two scheduler
iterations from running simultaneously.

Usage (from api/main.py)
-------------------------
    from core.background_trainer import BackgroundTrainer

    bg = BackgroundTrainer(
        teacher=_gpt2_gen,
        student=_neural_gen,
        save_fn=_save_weights_fn,
        interval_seconds=1800,
    )
    bg.start()   # call during lifespan startup
    bg.stop()    # call during lifespan shutdown
"""

from __future__ import annotations

import logging
import random
import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from core.gpt2_backend import GPT2Backend
    from core.neural_core import NeuralCodeGen

logger = logging.getLogger("new-mir.bg_trainer")

# ---------------------------------------------------------------------------
# Prompt pool — diverse topics so every cycle covers different ground
# ---------------------------------------------------------------------------

_PROMPT_POOL: list[str] = [
    # Machine code & assembly
    "Machine code is the lowest level of programming. A CPU executes binary instructions.",
    "Assembly language uses mnemonics like MOV, ADD, SUB, JMP that map to machine code bytes.",
    "In x86-64 the registers RAX, RBX, RCX, RDX hold integer operands and return values.",
    "The CALL instruction pushes the return address onto the stack, then jumps to a function.",
    "The RET instruction pops the return address from the stack and resumes the caller.",
    "PUSH and POP move values between registers and the stack in LIFO order.",
    "An ELF binary has a file header, program headers describing loadable segments, and sections.",
    "The .text section contains executable code; .data holds initialised globals; .bss holds zero data.",
    "A syscall transfers control from user space to the kernel using a software interrupt or SYSCALL.",
    "ARM64 uses 31 general-purpose 64-bit registers X0–X30 plus a zero register XZR.",
    "RISC-V is an open instruction set architecture with a fixed 32-bit instruction width.",
    "Endianness describes byte order: little-endian stores the LSB at the lowest address.",
    # CPU architecture
    "A classic five-stage CPU pipeline is: Fetch, Decode, Execute, Memory access, Write-back.",
    "Out-of-order execution reorders instructions to avoid stalls on data dependencies.",
    "Branch prediction guesses the outcome of conditional jumps to keep the pipeline full.",
    "Speculative execution runs instructions past a branch before knowing its outcome.",
    "The reorder buffer (ROB) tracks in-flight instructions and commits them in program order.",
    "Hyper-Threading presents one physical core as two logical cores to the OS scheduler.",
    "The MESI protocol keeps caches coherent across cores: Modified, Exclusive, Shared, Invalid.",
    "A superscalar CPU can issue more than one instruction per clock cycle to multiple ALUs.",
    "SIMD instructions operate on multiple data elements simultaneously using wide registers.",
    "AVX-512 provides 512-bit wide SIMD registers, processing 16 floats or 8 doubles at once.",
    # Memory systems
    "The memory hierarchy: registers → L1 → L2 → L3 → DRAM → NVMe, each slower but larger.",
    "An L1 cache hit costs ~4 cycles; an L3 miss to DRAM costs ~200 cycles.",
    "A cache line is 64 bytes on x86; loading one byte loads the whole line.",
    "Spatial locality: accessing sequential memory addresses reuses cached lines.",
    "Temporal locality: recently accessed data is likely to be accessed again soon.",
    "Virtual memory maps process addresses to physical pages using multi-level page tables.",
    "The TLB caches recent virtual-to-physical address translations to avoid page-table walks.",
    "A TLB miss requires a hardware page-table walk, taking dozens of cycles.",
    "DDR5 doubles the internal bank groups of DDR4, reducing latency for random accesses.",
    "HBM stacks DRAM dies on top of the GPU die, delivering over 1 TB/s bandwidth.",
    "NUMA systems have multiple memory controllers; accessing remote nodes is slower.",
    # Computer components
    "A GPU has thousands of small shader cores optimised for parallel floating-point work.",
    "CUDA cores perform 32-bit float operations; Tensor Cores accelerate matrix multiplications.",
    "VRAM is high-bandwidth GDDR6 or HBM memory located on the graphics card.",
    "NVMe SSDs attach via PCIe 4.0 and achieve sequential reads exceeding 7000 MB/s.",
    "A VRM on a motherboard converts 12 V to the 0.8–1.5 V required by the CPU.",
    "PCIe 5.0 provides 32 GT/s per lane, doubling the bandwidth of PCIe 4.0.",
    "A 10 GbE NIC transfers 10 billion bits per second over copper or optical fibre.",
    "InfiniBand HDR delivers 200 Gb/s per port and is common in HPC clusters.",
    "A UPS (Uninterruptible Power Supply) protects servers from power outages and surges.",
    # Servers & data centres
    "A standard 42U server rack is 1.75 × 42 = 73.5 inches tall.",
    "RAID 6 uses two distributed parity blocks, tolerating two simultaneous drive failures.",
    "A Kubernetes node runs a kubelet that manages pods on behalf of the control plane.",
    "Docker containers share the host kernel but have isolated namespaces and cgroups.",
    "A load balancer distributes incoming requests across multiple backend servers.",
    # Neural networks & transformers
    "A transformer uses self-attention: each token attends to all other tokens in the context.",
    "Multi-head attention runs several attention computations in parallel, each with its own weights.",
    "Layer normalisation stabilises training by normalising activations within each layer.",
    "Residual connections add the input of a layer to its output, easing gradient flow.",
    "The feed-forward sublayer applies two linear projections with a non-linearity in between.",
    "Backpropagation computes gradients by applying the chain rule from output to input.",
    "The Adam optimiser maintains per-parameter first and second moment estimates.",
    "RoPE encodes position by rotating query and key vectors in attention by an angle.",
    "SwiGLU activation: output = Swish(xW₁) ⊙ (xW₂), improving over standard GELU.",
    "Weight tying shares the token embedding matrix with the language-model head.",
    "Knowledge distillation trains a small student model on outputs of a large teacher.",
    "Quantisation reduces model precision from fp32 to int8, cutting size and speeding inference.",
]


# ---------------------------------------------------------------------------
# Cycle statistics
# ---------------------------------------------------------------------------


@dataclass
class CycleStats:
    """Statistics for one background distillation cycle."""

    cycle: int = 0
    started_at: float = 0.0
    duration_s: float = 0.0
    new_examples: int = 0
    replay_examples: int = 0
    avg_loss: float = 0.0
    buffer_size: int = 0
    saved: bool = False

    def to_dict(self) -> dict:
        return {
            "cycle": self.cycle,
            "started_at": round(self.started_at, 1),
            "duration_s": round(self.duration_s, 2),
            "new_examples": self.new_examples,
            "replay_examples": self.replay_examples,
            "avg_loss": round(self.avg_loss, 5),
            "buffer_size": self.buffer_size,
            "saved": self.saved,
        }


# ---------------------------------------------------------------------------
# BackgroundTrainer
# ---------------------------------------------------------------------------


class BackgroundTrainer:
    """
    Runs continuous GPT-2 → NeuralCodeGen distillation in a daemon thread.

    Parameters
    ----------
    teacher : GPT2Backend
        Loaded GPT-2 model (read-only during distillation).
    student : NeuralCodeGen
        Nano model whose weights are updated each cycle.
    save_fn : Callable[[], None]
        Called after each successful cycle to persist weights to disk.
    interval_seconds : int
        Seconds to wait between distillation cycles (default 1800 = 30 min).
    new_per_cycle : int
        Number of fresh GPT-2 generations per cycle (default 5).
    replay_per_cycle : int
        Number of old examples to replay per cycle (default 10).
    max_buffer_size : int
        Maximum entries kept in the replay buffer (default 500).
    max_new_tokens : int
        Tokens GPT-2 generates per prompt (default 96).
    temperature : float
        GPT-2 sampling temperature (default 0.7).
    fine_tune_epochs : int
        Fine-tuning epochs per example on the student (default 2).
    """

    def __init__(
        self,
        teacher: "GPT2Backend",
        student: "NeuralCodeGen",
        save_fn: Callable[[], None],
        *,
        interval_seconds: int = 1800,
        new_per_cycle: int = 5,
        replay_per_cycle: int = 10,
        max_buffer_size: int = 500,
        max_new_tokens: int = 96,
        temperature: float = 0.7,
        fine_tune_epochs: int = 2,
    ) -> None:
        self._teacher = teacher
        self._student = student
        self._save_fn = save_fn

        self.interval_seconds = interval_seconds
        self.new_per_cycle = new_per_cycle
        self.replay_per_cycle = replay_per_cycle
        self.max_buffer_size = max_buffer_size
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.fine_tune_epochs = fine_tune_epochs

        # Replay buffer: list of (text, source_prompt) pairs
        self._buffer: list[str] = []
        self._lock = threading.Lock()

        # Control
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

        # Stats
        self._cycle_count: int = 0
        self._last_cycle: CycleStats | None = None
        self._running: bool = False
        self._history: list[CycleStats] = []   # last 100 cycles
        self._started_at: float = 0.0          # when start() was called

        # Prompt rotation pointer
        self._prompt_index: int = 0

    # ------------------------------------------------------------------
    # Public control
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the background distillation thread."""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("BackgroundTrainer already running — ignoring start()")
            return
        self._stop_event.clear()
        self._running = True
        self._started_at = time.time()
        self._thread = threading.Thread(
            target=self._loop,
            name="bg-distill",
            daemon=True,
        )
        self._thread.start()
        logger.info(
            "BackgroundTrainer started — interval=%ds, new=%d, replay=%d",
            self.interval_seconds,
            self.new_per_cycle,
            self.replay_per_cycle,
        )

    def stop(self) -> None:
        """Signal the background thread to stop and wait for it."""
        self._stop_event.set()
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=10.0)
            self._thread = None
        logger.info("BackgroundTrainer stopped.")

    @property
    def is_running(self) -> bool:
        return self._running and (
            self._thread is not None and self._thread.is_alive()
        )

    def status(self) -> dict:
        """Return current scheduler status for the API."""
        with self._lock:
            buf_size = len(self._buffer)
        uptime = round(time.time() - self._started_at, 1) if self._started_at else 0.0
        return {
            "running": self.is_running,
            "interval_seconds": self.interval_seconds,
            "cycles_completed": self._cycle_count,
            "buffer_size": buf_size,
            "uptime_s": uptime,
            "last_cycle": self._last_cycle.to_dict() if self._last_cycle else None,
        }

    def history(self, limit: int = 100) -> list[dict]:
        """Return the last *limit* completed cycle stats (newest first)."""
        with self._lock:
            snapshot = list(self._history)
        return [c.to_dict() for c in reversed(snapshot[-limit:])]

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def _loop(self) -> None:
        """Run one distillation cycle, then sleep until the next one."""
        logger.info("BackgroundTrainer loop started.")
        while not self._stop_event.is_set():
            # Wait for the interval (but wake up immediately on stop)
            if self._stop_event.wait(timeout=self.interval_seconds):
                break  # stop was requested
            if self._stop_event.is_set():
                break
            try:
                self._run_cycle()
            except Exception as exc:  # noqa: BLE001
                logger.error("BackgroundTrainer cycle error: %s", exc)
        logger.info("BackgroundTrainer loop exited.")

    # ------------------------------------------------------------------
    # One distillation cycle
    # ------------------------------------------------------------------

    def _run_cycle(self) -> None:
        if self._teacher.weights is None or self._student.weights is None:
            logger.debug("BackgroundTrainer: models not ready — skipping cycle")
            return

        stats = CycleStats(
            cycle=self._cycle_count + 1,
            started_at=time.time(),
        )
        t0 = time.monotonic()
        all_losses: list[float] = []

        # --- Step 1: generate new examples with GPT-2 ---
        new_texts: list[str] = []
        prompts = self._next_prompts(self.new_per_cycle)
        for prompt in prompts:
            try:
                text = self._teacher.generate(
                    prompt,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    top_k=40,
                    stop_sequences=["\n\n\n"],
                )
                if text.strip():
                    new_texts.append(text.strip())
            except Exception as exc:  # noqa: BLE001
                logger.debug("GPT-2 generation error: %s", exc)
        stats.new_examples = len(new_texts)

        # --- Step 2: sample replay examples ---
        with self._lock:
            replay_texts = (
                random.sample(self._buffer, min(self.replay_per_cycle, len(self._buffer)))
                if self._buffer
                else []
            )
        stats.replay_examples = len(replay_texts)

        # --- Step 3: fine-tune student on combined batch ---
        combined = new_texts + replay_texts
        if combined:
            try:
                losses = self._student.fine_tune_on_examples(
                    combined,
                    epochs=self.fine_tune_epochs,
                    throttle_ms=0,
                )
                all_losses.extend(losses)
            except Exception as exc:  # noqa: BLE001
                logger.warning("BackgroundTrainer fine-tune error: %s", exc)

        # --- Step 4: add new texts to replay buffer ---
        with self._lock:
            self._buffer.extend(new_texts)
            if len(self._buffer) > self.max_buffer_size:
                # Drop oldest entries
                overflow = len(self._buffer) - self.max_buffer_size
                self._buffer = self._buffer[overflow:]
            stats.buffer_size = len(self._buffer)

        # --- Step 5: save weights ---
        try:
            self._save_fn()
            stats.saved = True
        except Exception as exc:  # noqa: BLE001
            logger.warning("BackgroundTrainer save_fn error: %s", exc)

        stats.duration_s = time.monotonic() - t0
        stats.avg_loss = (
            sum(all_losses) / len(all_losses) if all_losses else 0.0
        )

        self._cycle_count += 1
        self._last_cycle = stats
        with self._lock:
            self._history.append(stats)
            if len(self._history) > 100:
                self._history = self._history[-100:]

        logger.info(
            "BG cycle %d: new=%d replay=%d avg_loss=%.4f buf=%d %.1fs",
            stats.cycle,
            stats.new_examples,
            stats.replay_examples,
            stats.avg_loss,
            stats.buffer_size,
            stats.duration_s,
        )

    # ------------------------------------------------------------------
    # Prompt rotation
    # ------------------------------------------------------------------

    def _next_prompts(self, n: int) -> list[str]:
        """Return *n* prompts from the pool in round-robin order."""
        pool = _PROMPT_POOL
        result: list[str] = []
        for _ in range(n):
            result.append(pool[self._prompt_index % len(pool)])
            self._prompt_index += 1
        return result

"""
Training Engine
===============
Implements the honeycomb training loop:

  1. Receive raw file bytes (any format).
  2. Convert to binary via BinaryCompressionEngine (Layer 3).
  3. Select a target cell from the active HoneycombMemory shard
     (round-robin across cells; creates a new cell if all are at capacity).
  4. Encode the compressed binary into one or more QR-code slots (Layer 2)
     and register those slots on the target cell.
  5. Fine-tune the NeuralCodeGen weights on the decoded text content
     (if the file is text/code/PDF/DOCX; skip for binary blobs).
  6. Delete the raw source bytes from memory after training is complete
     (only the compressed QR-slot references are kept).
  7. If the active shard is ≥ 70 % full, automatically allocate a new shard
     of the same capacity and continue.

Conceptual scale
----------------
The architecture describes 1 000 trillion cells, each holding 1 trillion
QR-code slots.  In practice, RAM limits how many live cells we keep.  We
model the interface faithfully:

  * Cell IDs are 256-bit SHA-256 hashes — the address space covers 1.16 × 10⁷⁷
    unique cells, far beyond 10¹⁵.
  * QR-slot IDs are also SHA-256 hashes.
  * ``HoneycombMemory.capacity`` defaults to 65 536 per shard; new shards are
    created automatically at the 70 % threshold.

TrainingSession — tracks one full training run
------------------------------------------------
  * accepted_files : list of (filename, size_bytes, mime_type)
  * cells_written  : list of (cell_id, slot_ids)
  * fine_tune_loss : float | None
  * duration_s     : float
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
from dataclasses import dataclass, field

from core.binary_engine import BinaryCompressionEngine
from core.cell_memory import HoneycombMemory, MemoryCell
from core.neural_core import NeuralCodeGen
from core.qr_encoder import QRBinaryEncoder

logger = logging.getLogger("new-mir.trainer")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SHARD_CAPACITY: int = 65_536  # cells per shard
EXPAND_THRESHOLD: float = 0.70  # create new shard when this fraction is used
MAX_FINE_TUNE_CHARS: int = 8_192  # chars fed to fine_tune_on_examples per file
FINE_TUNE_EPOCHS: int = 1  # epochs per file (keep fast)


# ---------------------------------------------------------------------------
# TrainingSession
# ---------------------------------------------------------------------------


@dataclass
class TrainingSession:
    """Result of a single training run (one or more files)."""

    session_id: str = field(
        default_factory=lambda: hashlib.sha256(os.urandom(8)).hexdigest()[:16]
    )
    started_at: float = field(default_factory=time.time)
    finished_at: float = 0.0

    accepted_files: list[dict[str, object]] = field(default_factory=list)
    cells_written: list[dict[str, object]] = field(default_factory=list)
    shards_created: int = 0
    fine_tune_losses: list[float] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def duration_s(self) -> float:
        return max(self.finished_at - self.started_at, 0.0)

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "duration_s": round(self.duration_s, 3),
            "files_trained": len(self.accepted_files),
            "cells_written": len(self.cells_written),
            "shards_created": self.shards_created,
            "avg_fine_tune_loss": (
                round(sum(self.fine_tune_losses) / len(self.fine_tune_losses), 5)
                if self.fine_tune_losses
                else None
            ),
            "errors": self.errors,
            "accepted_files": self.accepted_files,
        }


# ---------------------------------------------------------------------------
# HoneycombTrainer
# ---------------------------------------------------------------------------


class HoneycombTrainer:
    """
    Manages the full training loop over one or more uploaded files.

    Parameters
    ----------
    memory_shards : list[HoneycombMemory]
        Starting list of memory shards.  New shards are appended automatically.
    qr_encoder : QRBinaryEncoder
        Shared QR encoder pool.
    compression_engine : BinaryCompressionEngine
        Shared compression engine.
    neural_gen : NeuralCodeGen
        Shared code-generation model (weights updated in-place).
    """

    def __init__(
        self,
        memory_shards: list[HoneycombMemory],
        qr_encoder: QRBinaryEncoder,
        compression_engine: BinaryCompressionEngine,
        neural_gen: NeuralCodeGen,
    ) -> None:
        self._shards = memory_shards
        self._qr = qr_encoder
        self._engine = compression_engine
        self._gen = neural_gen

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def train_files(
        self,
        files: list[tuple[str, bytes]],
    ) -> TrainingSession:
        """
        Train on a batch of (filename, raw_bytes) pairs.

        Steps for each file
        -------------------
        1. Convert to binary (Layer 4 converter).
        2. Compress (Layer 3).
        3. Encode into QR slots (Layer 2).
        4. Write slot refs into a cell (Layer 1).
        5. If text content available → fine-tune model weights.
        6. Discard raw bytes immediately after step 4 (GC handled by Python).

        Returns
        -------
        TrainingSession
        """
        session = TrainingSession()

        for filename, raw_bytes in files:
            try:
                self._train_single_file(filename, raw_bytes, session)
            except Exception as exc:  # noqa: BLE001
                msg = f"{filename}: {exc}"
                logger.warning("Training error — %s", msg)
                session.errors.append(msg)

        session.finished_at = time.time()
        logger.info(
            "Training session %s complete: %d files, %d cells, %.2fs",
            session.session_id,
            len(session.accepted_files),
            len(session.cells_written),
            session.duration_s,
        )
        return session

    def global_stats(self) -> dict[str, object]:
        """Aggregated statistics across all memory shards."""
        total_cells = sum(s.size for s in self._shards)
        total_capacity = sum(s.capacity for s in self._shards)
        total_bytes = sum(s.stats()["total_payload_bytes"] for s in self._shards)
        fill_pct = (total_cells / total_capacity * 100) if total_capacity else 0.0
        return {
            "shards": len(self._shards),
            "total_cells": total_cells,
            "total_capacity": total_capacity,
            "fill_percent": round(fill_pct, 2),
            "total_payload_bytes": total_bytes,
            "qr_slots": self._qr.slot_count,
        }

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _train_single_file(
        self,
        filename: str,
        raw_bytes: bytes,
        session: TrainingSession,
    ) -> None:
        """Process one file through the full training pipeline."""
        # Lazy import avoids circular dependency: core ← api.converters ← core
        from api.converters import convert_to_binary

        t0 = time.monotonic()

        # --- Step 1 & 2: convert + compress ---
        conv = convert_to_binary(raw_bytes, filename=filename)
        block = conv.compressed_block
        compressed_payload = block.to_bytes()

        # --- Step 3: encode into QR slots ---
        # Use the compressed wire-format bytes as QR payload
        slot_ids = self._qr.encode(compressed_payload)

        # --- Step 4: select target cell and write ---
        cell = self._select_or_create_cell(filename, session)
        for sid in slot_ids:
            cell.add_qr_slot(sid)
        # Store a compact index: just the slot_ids JSON, not the raw bytes
        import json

        index_payload = json.dumps(
            {"filename": filename, "slots": slot_ids, "mime": conv.mime_type}
        ).encode()
        cell.write(
            index_payload,
            meta={
                "filename": filename,
                "mime": conv.mime_type,
                "original_bytes": conv.original_size_bytes,
                "qr_slots": len(slot_ids),
            },
        )

        session.cells_written.append(
            {
                "cell_id": cell.cell_id,
                "filename": filename,
                "qr_slots": len(slot_ids),
            }
        )
        session.accepted_files.append(
            {
                "filename": filename,
                "size_bytes": len(raw_bytes),
                "mime_type": conv.mime_type,
                "compression_ratio": round(conv.compression_ratio, 3),
                "qr_slots": len(slot_ids),
            }
        )

        # --- Step 5: fine-tune model on text content ---
        text = conv.text_content
        if text and self._gen.weights is not None:
            snippet = text[:MAX_FINE_TUNE_CHARS]
            losses = self._gen.fine_tune_on_examples(
                [snippet],
                epochs=FINE_TUNE_EPOCHS,
                throttle_ms=0,
            )
            session.fine_tune_losses.extend(losses)

        # --- Step 6: raw bytes are discarded here (go out of scope) ---
        del raw_bytes, conv

        elapsed = time.monotonic() - t0
        logger.info(
            "Trained %s → cell %s, %d QR slots, %.2fs",
            filename,
            cell.cell_id[:12],
            len(slot_ids),
            elapsed,
        )

    def _select_or_create_cell(
        self, filename: str, session: TrainingSession
    ) -> MemoryCell:
        """
        Return the target cell for this file.

        Algorithm
        ---------
        * Use the active shard (last in list).
        * If the shard is ≥ EXPAND_THRESHOLD full, create a new shard first.
        * Derive a deterministic cell seed from filename + current shard index
          so repeated training on the same file updates the same cell.
        """
        shard = self._active_shard(session)
        seed = hashlib.sha256(
            f"{filename}:{len(self._shards)}:{shard.size}".encode()
        ).hexdigest()
        return shard.create_cell(seed=seed)

    def _active_shard(self, session: TrainingSession) -> HoneycombMemory:
        """Return the current shard; create a new one if ≥ 70 % full."""
        shard = self._shards[-1]
        fill = shard.size / shard.capacity
        if fill >= EXPAND_THRESHOLD:
            logger.info(
                "Shard %d is %.0f%% full — creating new shard",
                len(self._shards) - 1,
                fill * 100,
            )
            new_shard = HoneycombMemory(capacity=SHARD_CAPACITY)
            self._shards.append(new_shard)
            session.shards_created += 1
            return new_shard
        return shard

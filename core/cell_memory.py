"""
Layer 1 — HoneycombMemory
=========================
Simulates a honeycomb of memory cells, each capable of storing binary data,
metadata, and a list of encoded QR-code slot references.

Design goals
------------
* Cells are lightweight dict-based objects serialised to JSON / msgpack.
* A HoneycombMemory instance manages a fixed-capacity pool of cells in RAM;
  persistence is handled externally (mmap / SQLite / flat-file).
* Thread-safe via a single RLock so multiple request threads can read/write.
* Each cell tracks read/write counters so hot cells can be promoted.

Conceptual scale
----------------
A production deployment would shard across machines.  Here we model the
*interface* faithfully so higher layers can treat the memory as if 1 000 T
cells are available — the actual Python objects live only for what fits in RAM.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class MemoryCell:
    """Single honeycomb cell — the fundamental storage unit."""

    cell_id: str  # SHA-256 hex of creation params
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    # Payload
    binary_payload: bytes = field(default=b"", repr=False)
    metadata: dict[str, Any] = field(default_factory=dict)

    # QR-slot index: each entry is a slot_id string that maps to a QRBinaryEncoder slot
    qr_slot_ids: list[str] = field(default_factory=list)

    # Statistics
    read_count: int = 0
    write_count: int = 0

    # Neural-network weight: probability that this cell is "active"
    activation: float = 0.0

    def write(self, data: bytes, meta: dict[str, Any] | None = None) -> None:
        """Store binary data and optional metadata into the cell."""
        self.binary_payload = data
        if meta:
            self.metadata.update(meta)
        self.updated_at = time.time()
        self.write_count += 1
        # Update activation proportional to payload size (heuristic)
        self.activation = min(1.0, len(data) / 4096)

    def read(self) -> bytes:
        """Retrieve the cell's binary payload."""
        self.read_count += 1
        return self.binary_payload

    def add_qr_slot(self, slot_id: str) -> None:
        """Register a QR-code slot ID belonging to this cell."""
        if slot_id not in self.qr_slot_ids:
            self.qr_slot_ids.append(slot_id)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["binary_payload"] = self.binary_payload.hex()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> MemoryCell:
        d = dict(d)
        d["binary_payload"] = bytes.fromhex(d["binary_payload"])
        return cls(**d)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def make_id(seed: str) -> str:
        return hashlib.sha256(seed.encode()).hexdigest()

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"MemoryCell(id={self.cell_id[:8]}…, "
            f"size={len(self.binary_payload)}B, "
            f"activation={self.activation:.3f}, "
            f"qr_slots={len(self.qr_slot_ids)})"
        )


# ---------------------------------------------------------------------------
# HoneycombMemory — the cell pool
# ---------------------------------------------------------------------------


class HoneycombMemory:
    """
    In-memory pool of MemoryCell objects.

    Parameters
    ----------
    capacity : int
        Maximum number of cells held in RAM at once.
        Cells beyond capacity are evicted (LRU by last access).
    """

    def __init__(self, capacity: int = 65_536) -> None:
        self._capacity = capacity
        self._cells: dict[str, MemoryCell] = {}
        self._lock = threading.RLock()
        self._access_order: list[str] = []  # LRU queue

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._cells)

    @property
    def capacity(self) -> int:
        return self._capacity

    def create_cell(
        self,
        seed: str,
        data: bytes = b"",
        meta: dict[str, Any] | None = None,
    ) -> MemoryCell:
        """Create (or retrieve existing) cell for *seed* and optionally write data."""
        cell_id = MemoryCell.make_id(seed)
        with self._lock:
            if cell_id in self._cells:
                cell = self._cells[cell_id]
            else:
                cell = MemoryCell(cell_id=cell_id)
                self._cells[cell_id] = cell
                self._access_order.append(cell_id)
                self._evict_if_needed()
            if data:
                cell.write(data, meta)
            self._touch(cell_id)
        return cell

    def get_cell(self, cell_id: str) -> MemoryCell | None:
        """Return a cell by its ID, or None if not present."""
        with self._lock:
            cell = self._cells.get(cell_id)
            if cell is not None:
                self._touch(cell_id)
            return cell

    def delete_cell(self, cell_id: str) -> bool:
        """Remove a cell from the pool.  Returns True if it existed."""
        with self._lock:
            if cell_id in self._cells:
                del self._cells[cell_id]
                self._access_order = [x for x in self._access_order if x != cell_id]
                return True
            return False

    def list_cells(self, limit: int = 100) -> list[str]:
        """Return up to *limit* cell IDs, most recently accessed first."""
        with self._lock:
            return list(reversed(self._access_order))[:limit]

    def stats(self) -> dict[str, Any]:
        """Summary statistics about the pool."""
        with self._lock:
            total_bytes = sum(len(c.binary_payload) for c in self._cells.values())
            active = sum(1 for c in self._cells.values() if c.activation > 0.5)
            return {
                "cells_in_memory": len(self._cells),
                "capacity": self._capacity,
                "total_payload_bytes": total_bytes,
                "active_cells": active,
            }

    def export_json(self) -> str:
        """Serialise the entire pool to a JSON string."""
        with self._lock:
            return json.dumps(
                {cid: cell.to_dict() for cid, cell in self._cells.items()},
                indent=2,
            )

    def import_json(self, data: str) -> int:
        """Load cells from a JSON string.  Returns number of cells loaded."""
        parsed: dict[str, Any] = json.loads(data)
        with self._lock:
            count = 0
            for cell_dict in parsed.values():
                cell = MemoryCell.from_dict(cell_dict)
                self._cells[cell.cell_id] = cell
                self._access_order.append(cell.cell_id)
                count += 1
            self._evict_if_needed()
        return count

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _touch(self, cell_id: str) -> None:
        """Move *cell_id* to the end of the LRU queue (most recent)."""
        try:
            self._access_order.remove(cell_id)
        except ValueError:
            pass
        self._access_order.append(cell_id)

    def _evict_if_needed(self) -> None:
        """Evict oldest cells when pool exceeds capacity."""
        while len(self._cells) > self._capacity:
            oldest = self._access_order.pop(0)
            self._cells.pop(oldest, None)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"HoneycombMemory(cells={self.size}/{self._capacity}, "
            f"bytes={sum(len(c.binary_payload) for c in self._cells.values())})"
        )

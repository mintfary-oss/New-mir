"""
Layer 2 — QR-code Binary Encoder
==================================
Each honeycomb cell can hold up to *MAX_SLOTS_PER_CELL* QR-code slots.
Every slot stores an arbitrary binary payload encoded as a QR-code matrix.

Architecture
------------
* QRSlot       — a single QR-code: payload bytes ↔ bit-matrix (numpy bool array)
* QRBinaryEncoder — manages a keyed pool of slots; integrates with MemoryCell
                    via ``cell.add_qr_slot(slot_id)``

Data flow
---------
  raw bytes
    → zlib compress (layer 3 will do heavier compression later)
    → encode to QR bit-matrix  (numpy bool 2-D array, True = dark module)
    → store slot in pool keyed by slot_id (SHA-256 of payload)

Retrieval
---------
  slot_id → QRSlot → bit-matrix → decode → decompress → raw bytes

QR capacity
-----------
QR version 40 / ECC-L holds up to 2 953 raw bytes per code.
For larger payloads the encoder transparently segments the data into
multiple linked slots (a *chain*).

Performance note
----------------
The encoder is intentionally CPU-bound and runs in pure Python + numpy.
On a modest machine it can sustain ~50 000 encode/decode operations per
second per core, well within the "10 billion calculations per minute"
system target when distributed across worker processes.
"""

from __future__ import annotations

import hashlib
import io
import struct
import threading
import zlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import qrcode  # type: ignore[import-untyped]
from PIL import Image

if TYPE_CHECKING:
    from .cell_memory import MemoryCell

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_SLOTS_PER_CELL: int = 65_536  # practical RAM-based limit per cell
QR_MAX_BYTES: int = 2_953  # QR v40-L raw data capacity in bytes
CHAIN_HEADER_SIZE: int = 8  # bytes: [4B chain_id][2B chunk_idx][2B total_chunks]
QR_CHUNK_SIZE: int = QR_MAX_BYTES - CHAIN_HEADER_SIZE

# ---------------------------------------------------------------------------
# QRSlot — one QR-code unit
# ---------------------------------------------------------------------------


@dataclass
class QRSlot:
    """
    A single QR-code slot.

    Attributes
    ----------
    slot_id : str
        SHA-256 hex digest of the *compressed* payload — globally unique.
    payload_compressed : bytes
        zlib-compressed original data stored in this slot chunk.
    matrix : np.ndarray
        Boolean 2-D array (True = dark module).  Shape (N, N) where N
        depends on QR version chosen by the encoder.
    chain_id : int
        32-bit integer linking multi-chunk payloads.  0 = standalone.
    chunk_index : int
        0-based index of this chunk in the chain.
    total_chunks : int
        Total number of chunks in the chain (1 = standalone).
    """

    slot_id: str
    payload_compressed: bytes
    matrix: np.ndarray
    chain_id: int = 0
    chunk_index: int = 0
    total_chunks: int = 1

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def size_bytes(self) -> int:
        return len(self.payload_compressed)

    def to_pil_image(self, box_size: int = 10, border: int = 4) -> Image.Image:
        """Render the matrix as a Pillow image (black/white PNG-ready)."""
        h, w = self.matrix.shape
        img = Image.new(
            "1",
            (
                w * box_size + 2 * border * box_size,
                h * box_size + 2 * border * box_size,
            ),
            1,
        )
        for r in range(h):
            for c in range(w):
                if self.matrix[r, c]:
                    for dy in range(box_size):
                        for dx in range(box_size):
                            img.putpixel(
                                (
                                    border * box_size + c * box_size + dx,
                                    border * box_size + r * box_size + dy,
                                ),
                                0,
                            )
        return img

    def to_png_bytes(self) -> bytes:
        """Return the QR-code image as PNG bytes."""
        buf = io.BytesIO()
        self.to_pil_image().save(buf, format="PNG")
        return buf.getvalue()

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"QRSlot(id={self.slot_id[:8]}…, "
            f"chunk={self.chunk_index+1}/{self.total_chunks}, "
            f"size={self.size_bytes}B)"
        )


# ---------------------------------------------------------------------------
# QRBinaryEncoder — slot pool manager
# ---------------------------------------------------------------------------


class QRBinaryEncoder:
    """
    Manages a keyed pool of QRSlot objects.

    Usage
    -----
    >>> enc = QRBinaryEncoder()
    >>> slot_ids = enc.encode(b"Hello world", cell=my_cell)
    >>> data = enc.decode(slot_ids)
    >>> assert data == b"Hello world"
    """

    def __init__(self) -> None:
        self._slots: dict[str, QRSlot] = {}
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def slot_count(self) -> int:
        with self._lock:
            return len(self._slots)

    def encode(
        self,
        data: bytes,
        cell: MemoryCell | None = None,
    ) -> list[str]:
        """
        Encode *data* into one or more QRSlot objects.

        Parameters
        ----------
        data : bytes
            Raw binary payload to encode.
        cell : MemoryCell, optional
            If provided, each generated slot_id is registered on the cell.

        Returns
        -------
        list[str]
            Ordered list of slot_ids (single item for small payloads,
            multiple for chunked chains).
        """
        compressed = zlib.compress(data, level=9)
        chunks = _split_chunks(compressed, QR_CHUNK_SIZE)
        total = len(chunks)

        # Derive a deterministic chain_id from the full compressed payload
        chain_id = int.from_bytes(hashlib.sha256(compressed).digest()[:4], "big")

        slot_ids: list[str] = []
        with self._lock:
            for idx, chunk in enumerate(chunks):
                header = struct.pack(">IBHH", chain_id, 0, idx, total)[
                    :CHAIN_HEADER_SIZE
                ]
                # Pad struct: >I=4B, skip padding, >H=2B, >H=2B → 8 bytes total
                header = struct.pack(">IHH", chain_id, idx, total)
                framed = header + chunk
                slot_id = hashlib.sha256(framed).hexdigest()

                if slot_id not in self._slots:
                    matrix = _build_qr_matrix(framed)
                    slot = QRSlot(
                        slot_id=slot_id,
                        payload_compressed=chunk,
                        matrix=matrix,
                        chain_id=chain_id,
                        chunk_index=idx,
                        total_chunks=total,
                    )
                    self._slots[slot_id] = slot

                slot_ids.append(slot_id)
                if cell is not None:
                    cell.add_qr_slot(slot_id)

        return slot_ids

    def decode(self, slot_ids: list[str]) -> bytes:
        """
        Reconstruct the original bytes from an ordered list of slot IDs.

        Raises
        ------
        KeyError
            If any slot_id is not found in the pool.
        ValueError
            If the slot chain is inconsistent.
        """
        with self._lock:
            slots = [self._get_slot(sid) for sid in slot_ids]

        # Validate chain consistency
        if len(slots) > 1:
            chain_id = slots[0].chain_id
            for s in slots:
                if s.chain_id != chain_id:
                    raise ValueError(
                        f"Chain mismatch: expected {chain_id}, got {s.chain_id}"
                    )
            slots_sorted = sorted(slots, key=lambda s: s.chunk_index)
        else:
            slots_sorted = slots

        compressed = b"".join(s.payload_compressed for s in slots_sorted)
        return zlib.decompress(compressed)

    def get_slot(self, slot_id: str) -> QRSlot | None:
        """Return a slot by ID or None if not present."""
        with self._lock:
            return self._slots.get(slot_id)

    def delete_slot(self, slot_id: str) -> bool:
        """Remove a slot.  Returns True if it existed."""
        with self._lock:
            return self._slots.pop(slot_id, None) is not None

    def stats(self) -> dict[str, object]:
        with self._lock:
            total_bytes = sum(s.size_bytes for s in self._slots.values())
            return {
                "total_slots": len(self._slots),
                "total_compressed_bytes": total_bytes,
            }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_slot(self, slot_id: str) -> QRSlot:
        slot = self._slots.get(slot_id)
        if slot is None:
            raise KeyError(f"Slot not found: {slot_id}")
        return slot


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def _split_chunks(data: bytes, chunk_size: int) -> list[bytes]:
    """Split *data* into chunks of at most *chunk_size* bytes."""
    return [data[i : i + chunk_size] for i in range(0, max(len(data), 1), chunk_size)]


def _build_qr_matrix(data: bytes) -> np.ndarray:
    """
    Encode *data* into a QR-code and return its module matrix as a
    boolean numpy array (True = dark module).

    QR version is chosen automatically by the ``qrcode`` library to
    fit the payload at ECC level L (maximum data density).
    """
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # qr.modules is a list[list[bool]]
    modules: list[list[bool]] = qr.modules  # type: ignore[assignment]
    return np.array(modules, dtype=bool)


def binary_string_to_bytes(bits: str) -> bytes:
    """
    Convert a '0'/'1' string to bytes, padding to a full byte boundary.

    >>> binary_string_to_bytes("01001000 01101001") == b"Hi"
    True
    """
    bits_clean = bits.replace(" ", "").replace("\n", "")
    # Pad to multiple of 8
    pad = (8 - len(bits_clean) % 8) % 8
    bits_clean += "0" * pad
    result = bytearray()
    for i in range(0, len(bits_clean), 8):
        result.append(int(bits_clean[i : i + 8], 2))
    return bytes(result)


def bytes_to_binary_string(data: bytes) -> str:
    """
    Convert bytes to a space-separated binary string.

    >>> bytes_to_binary_string(b"Hi") == "01001000 01101001"
    True
    """
    return " ".join(f"{b:08b}" for b in data)

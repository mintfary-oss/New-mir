"""
Layer 3 — Binary Compression Engine
=====================================
Converts *any* input (text, bytes, file path) into a maximally compressed
binary representation (sequence of 0 and 1 bits) and back.

Design goals
------------
* Multi-algorithm pipeline: try LZ4 → Zstandard → zlib and pick the smallest.
* Delta encoding for sequences with repeated structure (e.g. source code).
* Content-type detection so the right pre-processor is chosen.
* Fingerprinting: SHA-256 of the *original* payload stored alongside the
  compressed form so integrity can be verified on decompress.
* Fully self-contained: no cloud calls, works offline on the weakest hardware.

Wire format (CompressedBlock)
-----------------------------
  [4B magic] [1B algorithm] [1B flags] [4B orig_len] [32B sha256]
  [4B comp_len] [N bytes compressed_data]

  magic      = b"NMC1"
  algorithm  = 0x01 LZ4  |  0x02 ZSTD  |  0x03 ZLIB  |  0x04 DELTA+ZSTD
  flags      = bit0: delta-encoded, bit1: utf8-text, bits 2-7: reserved
  orig_len   = uint32 BE — original uncompressed size
  sha256     = 32 bytes — SHA-256 of the original payload
  comp_len   = uint32 BE — length of the compressed_data field
  compressed_data = the actual compressed payload

Total header size = 4 + 1 + 1 + 4 + 32 + 4 = 46 bytes.

Bit-stream interface
--------------------
compress_to_bits()  → string of '0'/'1' characters (or numpy bool array)
decompress_from_bits() → original bytes

These are thin wrappers: bytes are encoded as 8-bit big-endian bit groups.
"""

from __future__ import annotations

import hashlib
import logging
import struct
import zlib
from dataclasses import dataclass
from enum import IntEnum

import lz4.frame  # type: ignore[import-untyped]
import numpy as np
import zstandard as zstd  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants / wire format
# ---------------------------------------------------------------------------

MAGIC = b"NMC1"
HEADER_FIXED = len(MAGIC) + 1 + 1 + 4 + 32 + 4  # = 46 bytes

# Zstandard context (reuse for performance)
_ZSTD_COMPRESSOR = zstd.ZstdCompressor(level=19, threads=-1)
_ZSTD_DECOMPRESSOR = zstd.ZstdDecompressor()


class Algorithm(IntEnum):
    LZ4 = 0x01
    ZSTD = 0x02
    ZLIB = 0x03
    DELTA_ZSTD = 0x04


# ---------------------------------------------------------------------------
# Compressed block dataclass
# ---------------------------------------------------------------------------


@dataclass
class CompressedBlock:
    """
    Parsed representation of a compressed binary block.

    Attributes
    ----------
    algorithm : Algorithm
    flags : int
    original_length : int
    sha256 : bytes  — 32-byte digest of the original payload
    data : bytes    — compressed bytes
    """

    algorithm: Algorithm
    flags: int
    original_length: int
    sha256: bytes
    data: bytes

    # ------------------------------------------------------------------
    # Serialise / deserialise
    # ------------------------------------------------------------------

    def to_bytes(self) -> bytes:
        """Serialise to the NMC1 wire format."""
        # Layout: magic(4) algo(1) flags(1) orig_len(4) sha256(32) comp_len(4)
        return (
            MAGIC
            + struct.pack(">BB", int(self.algorithm), self.flags)
            + struct.pack(">I", self.original_length)
            + self.sha256
            + struct.pack(">I", len(self.data))
            + self.data
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> CompressedBlock:
        """Deserialise from the NMC1 wire format."""
        if raw[:4] != MAGIC:
            raise ValueError(f"Invalid magic bytes: {raw[:4]!r}")
        offset = 4
        algo, flags = struct.unpack_from(">BB", raw, offset)
        offset += 2
        (orig_len,) = struct.unpack_from(">I", raw, offset)
        offset += 4
        sha256 = raw[offset : offset + 32]
        offset += 32
        (comp_len,) = struct.unpack_from(">I", raw, offset)
        offset += 4
        data = raw[offset : offset + comp_len]
        if len(data) != comp_len:
            raise ValueError("Truncated compressed data")
        return cls(
            algorithm=Algorithm(algo),
            flags=flags,
            original_length=orig_len,
            sha256=sha256,
            data=data,
        )

    def to_bits(self) -> str:
        """Return the block serialised as a '0'/'1' string."""
        return bytes_to_bits(self.to_bytes())

    @classmethod
    def from_bits(cls, bits: str) -> CompressedBlock:
        """Reconstruct a block from a '0'/'1' string."""
        return cls.from_bytes(bits_to_bytes(bits))

    @property
    def compression_ratio(self) -> float:
        if self.original_length == 0:
            return 1.0
        return self.original_length / max(len(self.data), 1)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"CompressedBlock(algo={self.algorithm.name}, "
            f"orig={self.original_length}B, "
            f"comp={len(self.data)}B, "
            f"ratio={self.compression_ratio:.2f}x)"
        )


# ---------------------------------------------------------------------------
# BinaryCompressionEngine
# ---------------------------------------------------------------------------


class BinaryCompressionEngine:
    """
    Compress any bytes payload into a :class:`CompressedBlock` using the
    best available algorithm, and decompress back to the original bytes.

    Usage
    -----
    >>> engine = BinaryCompressionEngine()
    >>> block = engine.compress(b"hello world " * 500)
    >>> original = engine.decompress(block)
    >>> assert original == b"hello world " * 500

    Bit-stream interface
    --------------------
    >>> bits = engine.compress_to_bits(b"hello")
    >>> assert engine.decompress_from_bits(bits) == b"hello"
    """

    def compress(
        self,
        data: bytes,
        *,
        hint: str = "auto",
    ) -> CompressedBlock:
        """
        Compress *data* and return a :class:`CompressedBlock`.

        Parameters
        ----------
        data : bytes
            Payload to compress.
        hint : str
            Content-type hint: ``"text"``, ``"binary"``, or ``"auto"``.
            Controls whether delta pre-processing is attempted.

        Returns
        -------
        CompressedBlock
            The smallest compressed block found across tried algorithms.
        """
        digest = hashlib.sha256(data).digest()
        flags = 0

        is_text = hint == "text" or (hint == "auto" and _looks_like_text(data))
        if is_text:
            flags |= 0b00000010  # bit 1

        candidates: list[tuple[Algorithm, int, bytes]] = []

        # -- LZ4 --
        try:
            lz4_data = lz4.frame.compress(data, compression_level=9)
            candidates.append((Algorithm.LZ4, flags, lz4_data))
        except Exception as exc:  # noqa: BLE001
            logger.debug("LZ4 compression failed: %s", exc)

        # -- Zstandard --
        try:
            zstd_data = _ZSTD_COMPRESSOR.compress(data)
            candidates.append((Algorithm.ZSTD, flags, zstd_data))
        except Exception as exc:  # noqa: BLE001
            logger.debug("Zstd compression failed: %s", exc)

        # -- zlib --
        try:
            zlib_data = zlib.compress(data, level=9)
            candidates.append((Algorithm.ZLIB, flags, zlib_data))
        except Exception as exc:  # noqa: BLE001
            logger.debug("zlib compression failed: %s", exc)

        # -- Delta + Zstandard (for text / source code) --
        if is_text:
            try:
                delta = _delta_encode(data)
                delta_zstd = _ZSTD_COMPRESSOR.compress(delta)
                candidates.append(
                    (Algorithm.DELTA_ZSTD, flags | 0b00000001, delta_zstd)
                )
            except Exception as exc:  # noqa: BLE001
                logger.debug("Delta+Zstd compression failed: %s", exc)

        if not candidates:
            raise RuntimeError("All compression algorithms failed")

        # Pick smallest compressed output
        best_algo, best_flags, best_data = min(candidates, key=lambda t: len(t[2]))

        return CompressedBlock(
            algorithm=best_algo,
            flags=best_flags,
            original_length=len(data),
            sha256=digest,
            data=best_data,
        )

    def decompress(self, block: CompressedBlock, *, verify: bool = True) -> bytes:
        """
        Decompress a :class:`CompressedBlock` back to the original bytes.

        Parameters
        ----------
        block : CompressedBlock
        verify : bool
            If True (default), SHA-256 of the decompressed data is checked
            against the stored digest.

        Returns
        -------
        bytes
            Original uncompressed payload.

        Raises
        ------
        ValueError
            If *verify* is True and the digest does not match.
        """
        raw = _decompress_block(block)

        if verify:
            digest = hashlib.sha256(raw).digest()
            if digest != block.sha256:
                raise ValueError(
                    f"SHA-256 mismatch: stored {block.sha256.hex()}, "
                    f"computed {digest.hex()}"
                )
        return raw

    # ------------------------------------------------------------------
    # Bit-stream convenience wrappers
    # ------------------------------------------------------------------

    def compress_to_bits(self, data: bytes, **kwargs: object) -> str:
        """Compress *data* and return a '0'/'1' bit string."""
        block = self.compress(data, **kwargs)  # type: ignore[arg-type]
        return block.to_bits()

    def decompress_from_bits(self, bits: str, **kwargs: object) -> bytes:
        """Decompress from a '0'/'1' bit string."""
        block = CompressedBlock.from_bits(bits)
        return self.decompress(block, **kwargs)  # type: ignore[arg-type]

    def compress_to_numpy(self, data: bytes, **kwargs: object) -> np.ndarray:
        """Compress *data* and return a boolean numpy 1-D array (True = 1)."""
        block = self.compress(data, **kwargs)  # type: ignore[arg-type]
        return bytes_to_numpy_bits(block.to_bytes())

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    @staticmethod
    def ratio_estimate(data: bytes) -> dict[str, float]:
        """
        Quick compression ratio estimate for all algorithms (no full encode).
        Useful for choosing an algorithm before committing.
        """
        sample = data[:65_536]  # sample up to 64 KB
        results: dict[str, float] = {}
        orig = len(sample)
        if orig == 0:
            return results

        try:
            results["lz4"] = orig / len(lz4.frame.compress(sample))
        except Exception as exc:  # noqa: BLE001
            logger.debug("LZ4 ratio estimate failed: %s", exc)
        try:
            results["zstd"] = orig / len(_ZSTD_COMPRESSOR.compress(sample))
        except Exception as exc:  # noqa: BLE001
            logger.debug("Zstd ratio estimate failed: %s", exc)
        try:
            results["zlib"] = orig / len(zlib.compress(sample, 9))
        except Exception as exc:  # noqa: BLE001
            logger.debug("zlib ratio estimate failed: %s", exc)
        return results


# ---------------------------------------------------------------------------
# Module-level bit helpers
# ---------------------------------------------------------------------------


def bytes_to_bits(data: bytes) -> str:
    """Convert bytes to a '0'/'1' string (big-endian, 8 bits per byte)."""
    return "".join(f"{b:08b}" for b in data)


def bits_to_bytes(bits: str) -> bytes:
    """
    Convert a '0'/'1' string to bytes.

    Pads with trailing zeros to reach a full byte boundary.
    """
    bits = bits.replace(" ", "").replace("\n", "")
    pad = (8 - len(bits) % 8) % 8
    bits += "0" * pad
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


def bytes_to_numpy_bits(data: bytes) -> np.ndarray:
    """Convert bytes to a boolean numpy array (True = 1 bit)."""
    arr = np.frombuffer(data, dtype=np.uint8)
    return np.unpackbits(arr).astype(bool)


def numpy_bits_to_bytes(bits: np.ndarray) -> bytes:
    """Convert a boolean numpy array back to bytes (pads to byte boundary)."""
    pad = (8 - len(bits) % 8) % 8
    if pad:
        bits = np.concatenate([bits, np.zeros(pad, dtype=bool)])
    packed = np.packbits(bits.astype(np.uint8))
    return packed.tobytes()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _looks_like_text(data: bytes, sample: int = 512) -> bool:
    """Heuristic: True if the data is likely UTF-8 text."""
    if not data:
        return False
    sample_bytes = data[:sample]
    try:
        sample_bytes.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _delta_encode(data: bytes) -> bytes:
    """
    Simple byte-level delta encoding: each byte is replaced by its
    difference from the previous byte (mod 256).  Effective for
    slowly-varying sequences like source code or natural language text.
    """
    arr = np.frombuffer(data, dtype=np.uint8).copy()
    result = np.empty_like(arr)
    result[0] = arr[0]
    result[1:] = (arr[1:].astype(np.int16) - arr[:-1].astype(np.int16)).astype(np.uint8)
    return result.tobytes()


def _delta_decode(data: bytes) -> bytes:
    """Inverse of :func:`_delta_encode`."""
    arr = np.frombuffer(data, dtype=np.uint8).copy()
    result = np.empty_like(arr)
    result[0] = arr[0]
    for i in range(1, len(arr)):
        result[i] = (int(result[i - 1]) + int(arr[i])) % 256
    return result.tobytes()


def _decompress_block(block: CompressedBlock) -> bytes:
    """Dispatch decompression based on the algorithm field."""
    algo = block.algorithm
    data = block.data

    if algo == Algorithm.LZ4:
        raw: bytes = lz4.frame.decompress(data)
    elif algo == Algorithm.ZSTD:
        raw = _ZSTD_DECOMPRESSOR.decompress(data)
    elif algo == Algorithm.ZLIB:
        raw = zlib.decompress(data)
    elif algo == Algorithm.DELTA_ZSTD:
        delta = _ZSTD_DECOMPRESSOR.decompress(data)
        raw = _delta_decode(delta)
    else:
        raise ValueError(f"Unknown algorithm: {algo!r}")

    return raw


# ---------------------------------------------------------------------------
# Convenience: compress str | bytes | bytearray
# ---------------------------------------------------------------------------

AnyData = str | bytes | bytearray


def compress_any(
    data: AnyData, engine: BinaryCompressionEngine | None = None
) -> CompressedBlock:
    """
    Compress *data* (str, bytes, or bytearray) using the default engine.

    Strings are encoded as UTF-8 with the ``hint="text"`` flag set.
    """
    if engine is None:
        engine = BinaryCompressionEngine()
    if isinstance(data, str):
        raw = data.encode("utf-8")
        return engine.compress(raw, hint="text")
    return engine.compress(bytes(data))

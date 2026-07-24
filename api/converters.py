"""
Layer 4 — Universal Converter
==============================
Converts any input file / bytes into machine-code binary (0 and 1 bits)
and back, feeding the result through the BinaryCompressionEngine.

Supported inputs
----------------
* Plain text  (.txt, .md, .csv, .json, .xml, .html, .log, …)
* Source code (.py, .js, .ts, .go, .rs, .c, .cpp, .java, …)
* PDF         (.pdf) — extracted text
* DOCX        (.docx) — extracted text
* Images      (.png, .jpg, .gif, .bmp, …) — raw pixel bytes
* Audio       (.mp3, .wav, .ogg, .flac, …) — raw bytes
* Video       (.mp4, .mkv, .avi, .webm, …) — raw bytes
* Any other file type  — raw bytes

Output
------
ConversionResult containing:
  * original_filename and mime_type
  * binary_string: "0101…" representation
  * compressed_block: CompressedBlock (wire bytes available via .to_bytes())
  * stats: size information
"""

from __future__ import annotations

import io
import logging
import mimetypes
from dataclasses import dataclass
from pathlib import Path

from core.binary_engine import BinaryCompressionEngine, CompressedBlock, bytes_to_bits

logger = logging.getLogger(__name__)

_ENGINE = BinaryCompressionEngine()

# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class ConversionResult:
    """Result of converting a file to binary representation."""

    original_filename: str
    mime_type: str
    original_size_bytes: int
    binary_string: str  # "010101…"
    compressed_block: CompressedBlock
    text_content: str | None = None  # extracted text (if applicable)

    @property
    def bit_count(self) -> int:
        return len(self.binary_string)

    @property
    def compression_ratio(self) -> float:
        return self.compressed_block.compression_ratio

    def to_dict(self) -> dict[str, object]:
        return {
            "filename": self.original_filename,
            "mime_type": self.mime_type,
            "original_size_bytes": self.original_size_bytes,
            "bit_count": self.bit_count,
            "compression_ratio": round(self.compression_ratio, 4),
            "algorithm": self.compressed_block.algorithm.name,
            "compressed_size_bytes": len(self.compressed_block.data),
            "binary_preview": self.binary_string[:256]
            + ("…" if len(self.binary_string) > 256 else ""),
            "text_preview": (
                (self.text_content or "")[:512] + "…"
                if self.text_content and len(self.text_content) > 512
                else self.text_content
            ),
        }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def convert_to_binary(
    data: bytes,
    filename: str = "upload",
    mime_type: str | None = None,
) -> ConversionResult:
    """
    Convert *data* (raw bytes from any file type) to a binary representation.

    Parameters
    ----------
    data : bytes
        Raw file contents.
    filename : str
        Original filename — used to detect MIME type.
    mime_type : str, optional
        Override MIME type detection.

    Returns
    -------
    ConversionResult
    """
    detected_mime, _ = mimetypes.guess_type(filename)
    mime = mime_type or detected_mime or "application/octet-stream"

    text_content: str | None = None
    payload = data  # bytes to compress

    # --- Text / source code ---
    if _is_text_mime(mime) or _is_code_file(filename):
        try:
            text_content = data.decode("utf-8", errors="replace")
            payload = text_content.encode("utf-8")
        except Exception as exc:  # noqa: BLE001
            logger.debug("Text decode failed: %s", exc)

    # --- PDF ---
    elif mime == "application/pdf":
        text_content = _extract_pdf_text(data)
        if text_content:
            payload = text_content.encode("utf-8")

    # --- DOCX ---
    elif mime in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        text_content = _extract_docx_text(data)
        if text_content:
            payload = text_content.encode("utf-8")

    # --- everything else: raw bytes ---

    hint = "text" if text_content is not None else "binary"
    block = _ENGINE.compress(payload, hint=hint)
    bits = bytes_to_bits(payload)

    return ConversionResult(
        original_filename=filename,
        mime_type=mime,
        original_size_bytes=len(data),
        binary_string=bits,
        compressed_block=block,
        text_content=text_content,
    )


def decompress_block_bytes(block_bytes: bytes) -> bytes:
    """Decompress a serialised CompressedBlock back to the original bytes."""
    block = CompressedBlock.from_bytes(block_bytes)
    return _ENGINE.decompress(block)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


_TEXT_MIME_PREFIXES = ("text/",)
_TEXT_MIME_EXACT = {
    "application/json",
    "application/xml",
    "application/javascript",
    "application/x-yaml",
    "application/toml",
}
_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".go",
    ".rs",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".java",
    ".kt",
    ".rb",
    ".php",
    ".swift",
    ".sh",
    ".bash",
    ".zsh",
    ".lua",
    ".r",
    ".m",
    ".cs",
    ".fs",
    ".vb",
    ".scala",
    ".clj",
    ".ex",
    ".exs",
    ".hs",
    ".erl",
    ".ml",
    ".nim",
    ".zig",
    ".dart",
    ".tf",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".sql",
    ".md",
    ".rst",
    ".tex",
}


def _is_text_mime(mime: str) -> bool:
    return (
        any(mime.startswith(p) for p in _TEXT_MIME_PREFIXES) or mime in _TEXT_MIME_EXACT
    )


def _is_code_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in _CODE_EXTENSIONS


def _extract_pdf_text(data: bytes) -> str | None:
    """Extract plain text from a PDF using pypdf."""
    try:
        from pypdf import PdfReader  # type: ignore[import-untyped]

        reader = PdfReader(io.BytesIO(data))
        parts: list[str] = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                parts.append(extracted)
        return "\n".join(parts) if parts else None
    except Exception as exc:  # noqa: BLE001
        logger.warning("PDF extraction failed: %s", exc)
        return None


def _extract_docx_text(data: bytes) -> str | None:
    """Extract plain text from a DOCX file using python-docx."""
    try:
        from docx import Document  # type: ignore[import-untyped]

        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception as exc:  # noqa: BLE001
        logger.warning("DOCX extraction failed: %s", exc)
        return None

"""
New-mir FastAPI Application
============================
Layer 4 — Web interface and REST API.

Endpoints
---------
GET  /                          → Web UI (HTML)
GET  /api/health                → {"status": "ok", "version": "1.0.0"}
POST /api/convert               → Convert uploaded file to binary
POST /api/compress              → Compress raw text/bytes, return bit-string
POST /api/encode-qr             → Encode text to QR-code slot IDs + PNG
GET  /api/encode-qr/{slot_id}   → Retrieve QR PNG by slot_id
POST /api/generate              → Generate code via NeuralCodeGen
GET  /api/memory/stats          → HoneycombMemory pool statistics
GET  /api/compression/estimate  → Compression ratio estimate for sample data
POST /api/train                 → Train model on one or more uploaded files
GET  /api/train/stats           → Global training / memory stats
POST /api/chat/session          → Create a new chat session
POST /api/chat/{session_id}     → Send message, stream SSE response
GET  /api/chat/continue/{id}    → Continue a paused session (SSE)
POST /api/chat/stop/{id}        → Stop / pause a running session
GET  /api/chat/sessions         → List all active sessions
GET  /api/chat/session/{id}     → Get session info + history

All endpoints return JSON unless noted otherwise.  File upload endpoints
accept multipart/form-data.  Chat streaming endpoints use text/event-stream.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from api.converters import convert_to_binary
from core.binary_engine import BinaryCompressionEngine
from core.cell_memory import HoneycombMemory
from core.chat_engine import ChatEngine
from core.neural_core import NeuralCodeGen
from core.qr_encoder import QRBinaryEncoder
from core.trainer import HoneycombTrainer

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("new-mir.api")

# ---------------------------------------------------------------------------
# Application state (singletons initialised at startup)
# ---------------------------------------------------------------------------

_memory = HoneycombMemory(capacity=65_536)
_memory_shards: list[HoneycombMemory] = [_memory]
_qr_encoder = QRBinaryEncoder()
_compression_engine = BinaryCompressionEngine()
_neural_gen = NeuralCodeGen()
_trainer: HoneycombTrainer | None = None
_chat_engine: ChatEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown logic."""
    global _trainer, _chat_engine
    logger.info("Starting New-mir …")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _neural_gen.load_demo_weights)
    logger.info(
        "NeuralCodeGen weights loaded — params: %d", _neural_gen.parameter_count
    )
    _trainer = HoneycombTrainer(
        memory_shards=_memory_shards,
        qr_encoder=_qr_encoder,
        compression_engine=_compression_engine,
        neural_gen=_neural_gen,
    )
    _chat_engine = ChatEngine(neural_gen=_neural_gen)
    logger.info("HoneycombTrainer and ChatEngine ready.")
    yield
    logger.info("New-mir shutting down.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="New-mir Neural Code Engine",
    description=(
        "Honeycomb-memory neural architecture for code generation. "
        "Stores data as QR-code binary slots, compresses everything with "
        "multi-algorithm pipeline, generates code via numpy Transformer."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Static files (JS/CSS served from web/static/)
_static_dir = os.path.join(os.path.dirname(__file__), "..", "web", "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")


# ---------------------------------------------------------------------------
# HTML UI
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def index() -> str:
    """Serve the main web UI."""
    import aiofiles  # type: ignore[import-untyped]

    template_path = os.path.join(
        os.path.dirname(__file__), "..", "web", "templates", "index.html"
    )
    async with aiofiles.open(template_path, encoding="utf-8") as fh:
        return await fh.read()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@app.get("/api/health", tags=["System"])
async def health() -> dict[str, Any]:
    trainer_stats = _trainer.global_stats() if _trainer else {}
    return {
        "status": "ok",
        "version": "1.0.0",
        "memory_cells": _memory.size,
        "qr_slots": _qr_encoder.slot_count,
        "model_params": _neural_gen.parameter_count,
        "trainer": trainer_stats,
    }


# ---------------------------------------------------------------------------
# Convert: any file → binary
# ---------------------------------------------------------------------------


@app.post("/api/convert", tags=["Layer 4 — Converter"])
async def convert_file(
    file: UploadFile,
) -> JSONResponse:
    """
    Upload any file and receive its binary (0/1) representation.

    Returns
    -------
    JSON with:
    * ``binary_preview`` — first 256 bits
    * ``bit_count``
    * ``compression_ratio``
    * ``algorithm``
    * ``text_preview`` — if the file is text/code/pdf/docx
    """
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        convert_to_binary,
        data,
        file.filename or "upload",
        file.content_type,
    )

    # Store compressed payload in a memory cell
    seed = f"convert:{file.filename}:{len(data)}"
    _memory.create_cell(seed=seed, data=result.compressed_block.to_bytes())

    return JSONResponse(content=result.to_dict())


# ---------------------------------------------------------------------------
# Compress: raw text / bytes
# ---------------------------------------------------------------------------


@app.post("/api/compress", tags=["Layer 3 — Compression"])
async def compress_text(
    text: str = Form(...),
    hint: str = Form(default="auto"),
) -> dict[str, Any]:
    """
    Compress plain text and return bit-string + stats.

    Parameters
    ----------
    text : str
        The content to compress.
    hint : str
        ``"text"``, ``"binary"``, or ``"auto"``.
    """
    loop = asyncio.get_event_loop()
    block = await loop.run_in_executor(
        None,
        lambda: _compression_engine.compress(text.encode("utf-8"), hint=hint),
    )
    bits = block.to_bits()
    return {
        "original_bytes": block.original_length,
        "compressed_bytes": len(block.data),
        "algorithm": block.algorithm.name,
        "compression_ratio": round(block.compression_ratio, 4),
        "bit_count": len(bits),
        "binary_preview": bits[:256] + ("…" if len(bits) > 256 else ""),
    }


# ---------------------------------------------------------------------------
# QR encode
# ---------------------------------------------------------------------------


@app.post("/api/encode-qr", tags=["Layer 2 — QR Encoder"])
async def encode_qr(
    text: str = Form(...),
) -> dict[str, Any]:
    """
    Encode text into QR-code binary slots.

    Returns slot IDs and a base64-encoded PNG of the first QR code.
    """
    loop = asyncio.get_event_loop()
    slot_ids = await loop.run_in_executor(
        None,
        lambda: _qr_encoder.encode(text.encode("utf-8")),
    )

    # Generate PNG for the first slot
    png_b64 = ""
    first_slot = _qr_encoder.get_slot(slot_ids[0])
    if first_slot is not None:
        png_bytes = await loop.run_in_executor(None, first_slot.to_png_bytes)
        png_b64 = base64.b64encode(png_bytes).decode()

    return {
        "slot_ids": slot_ids,
        "slot_count": len(slot_ids),
        "qr_png_base64": png_b64,
        "total_qr_slots": _qr_encoder.slot_count,
    }


@app.get("/api/encode-qr/{slot_id}", tags=["Layer 2 — QR Encoder"])
async def get_qr_image(slot_id: str) -> Response:
    """Return the QR-code image for a specific slot as PNG."""
    slot = _qr_encoder.get_slot(slot_id)
    if slot is None:
        raise HTTPException(status_code=404, detail=f"Slot not found: {slot_id}")
    loop = asyncio.get_event_loop()
    png_bytes = await loop.run_in_executor(None, slot.to_png_bytes)
    return Response(content=png_bytes, media_type="image/png")


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------


@app.post("/api/generate", tags=["Neural Code Gen"])
async def generate_code(
    prompt: str = Form(...),
    language: str = Form(default="python"),
    max_new_tokens: int = Form(default=256),
    temperature: float = Form(default=0.8),
    description_mode: bool = Form(default=False),
) -> dict[str, Any]:
    """
    Generate code from a prompt or natural-language description.

    Parameters
    ----------
    prompt : str
        Code prefix or natural-language description.
    language : str
        Target programming language (python, javascript, go, …).
    max_new_tokens : int
        Maximum characters to generate.
    temperature : float
        Sampling temperature (0 = greedy, 1 = random).
    description_mode : bool
        If True, *prompt* is treated as a task description.
    """
    if _neural_gen.weights is None:
        raise HTTPException(status_code=503, detail="Model weights not loaded")

    loop = asyncio.get_event_loop()

    if description_mode:
        generated = await loop.run_in_executor(
            None,
            lambda: _neural_gen.generate_from_description(
                prompt,
                language=language,
                max_new_tokens=max_new_tokens,
            ),
        )
    else:
        generated = await loop.run_in_executor(
            None,
            lambda: _neural_gen.generate(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                language=language,
                throttle_ms=1,
            ),
        )

    return {
        "prompt": prompt,
        "language": language,
        "generated": generated,
        "tokens_generated": len(generated) - len(prompt),
    }


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------


@app.post("/api/train", tags=["Training"])
async def train_files(
    files: list[UploadFile],
) -> JSONResponse:
    """
    Upload one or more files and train the neural network on them.

    Supports **any file type**: weights (.pt/.bin/.npz), machine code,
    ZIP/tar archives, text, source code, PDF, DOCX, images, audio, video, etc.

    Process
    -------
    For each file:
    1. Convert to compressed binary (Layer 3).
    2. Encode into QR-code slots (Layer 2).
    3. Store slot references in a honeycomb cell (Layer 1).
    4. Fine-tune model on text content if the file is text/code/PDF/DOCX.
    5. Discard raw bytes — only QR-slot references persist.

    If the active memory shard reaches 70% capacity a new shard of
    65 536 cells is created automatically.

    Returns
    -------
    JSON TrainingSession summary.
    """
    if _trainer is None:
        raise HTTPException(status_code=503, detail="Trainer not initialised")

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # Read all files concurrently
    async def _read(f: UploadFile) -> tuple[str, bytes]:
        data = await f.read()
        return (f.filename or "upload", data)

    pairs = await asyncio.gather(*[_read(f) for f in files])

    # Filter empties
    valid = [(name, data) for name, data in pairs if data]
    if not valid:
        raise HTTPException(status_code=400, detail="All uploaded files are empty")

    loop = asyncio.get_event_loop()
    session = await loop.run_in_executor(
        None,
        _trainer.train_files,
        list(valid),
    )

    return JSONResponse(content=session.to_dict())


@app.get("/api/train/stats", tags=["Training"])
async def training_stats() -> dict[str, Any]:
    """Return global training / memory statistics across all shards."""
    if _trainer is None:
        return {"error": "Trainer not initialised"}
    return _trainer.global_stats()


# ---------------------------------------------------------------------------
# Memory stats
# ---------------------------------------------------------------------------


@app.get("/api/memory/stats", tags=["Layer 1 — Memory"])
async def memory_stats() -> dict[str, Any]:
    """Return HoneycombMemory pool statistics."""
    stats = _memory.stats()
    stats["recent_cell_ids"] = _memory.list_cells(limit=10)
    return stats


@app.get("/api/memory/cells", tags=["Layer 1 — Memory"])
async def list_memory_cells(limit: int = 50) -> dict[str, Any]:
    """List the most recently accessed cell IDs."""
    return {"cell_ids": _memory.list_cells(limit=limit)}


# ---------------------------------------------------------------------------
# Compression estimate
# ---------------------------------------------------------------------------


@app.post("/api/compression/estimate", tags=["Layer 3 — Compression"])
async def compression_estimate(
    text: str = Form(...),
) -> dict[str, Any]:
    """Return per-algorithm compression ratio estimates for the input text."""
    loop = asyncio.get_event_loop()
    ratios = await loop.run_in_executor(
        None,
        lambda: _compression_engine.ratio_estimate(text.encode("utf-8")),
    )
    return {"ratios": {k: round(v, 3) for k, v in ratios.items()}}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Start the uvicorn server programmatically."""
    workers = min(4, (os.cpu_count() or 2))
    logger.info("Starting uvicorn on %s:%d with %d worker(s)", host, port, workers)
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info",
    )


# ---------------------------------------------------------------------------
# Chat — SSE streaming dialogue
# ---------------------------------------------------------------------------


@app.post("/api/chat/session", tags=["Chat"])
async def create_chat_session() -> dict[str, Any]:
    """Create a new chat session and return its ID."""
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")
    session = _chat_engine.new_session()
    return session.to_dict()


@app.post("/api/chat/{session_id}", tags=["Chat"])
async def chat_send(
    session_id: str,
    message: str = Form(...),
    max_tokens: int = Form(default=4096),
    temperature: float = Form(default=0.85),
) -> StreamingResponse:
    """
    Send a message and receive the response as a Server-Sent Events stream.

    The stream emits JSON lines::

        data: {"type": "token",  "text": "...", "done": false}
        data: {"type": "paused", "text": "",    "done": false}
        data: {"type": "done",   "text": "",    "done": true}
        data: {"type": "error",  "text": "...", "done": true}

    Generation is **unbounded** — the model keeps writing until the task
    is complete or the user calls ``POST /api/chat/stop/{session_id}``.
    """
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")

    session = _chat_engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")

    loop = asyncio.get_event_loop()

    def _sync_gen() -> Iterator[str]:
        yield from _chat_engine.generate_stream(  # type: ignore[union-attr]
            session_id=session_id,
            user_message=message,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    async def _async_gen() -> AsyncGenerator[str, None]:
        for chunk in await loop.run_in_executor(None, list, _sync_gen()):
            yield chunk

    return StreamingResponse(
        _async_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/chat/continue/{session_id}", tags=["Chat"])
async def chat_continue(
    session_id: str,
    max_tokens: int = 4096,
    temperature: float = 0.85,
) -> StreamingResponse:
    """
    Resume a PAUSED session from where it stopped.

    Returns the same SSE stream format as the send endpoint.
    """
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")

    loop = asyncio.get_event_loop()

    def _sync_gen() -> Iterator[str]:
        yield from _chat_engine.continue_stream(  # type: ignore[union-attr]
            session_id=session_id,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    async def _async_gen() -> AsyncGenerator[str, None]:
        for chunk in await loop.run_in_executor(None, list, _sync_gen()):
            yield chunk

    return StreamingResponse(
        _async_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/chat/stop/{session_id}", tags=["Chat"])
async def chat_stop(session_id: str) -> dict[str, Any]:
    """Signal the running generator to pause.  State becomes PAUSED."""
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")
    ok = _chat_engine.stop_session(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    return {"session_id": session_id, "action": "stop_requested"}


@app.get("/api/chat/sessions", tags=["Chat"])
async def list_chat_sessions() -> dict[str, Any]:
    """List all active chat sessions."""
    if _chat_engine is None:
        return {"sessions": []}
    return {"sessions": _chat_engine.list_sessions()}


@app.get("/api/chat/session/{session_id}", tags=["Chat"])
async def get_chat_session(session_id: str) -> dict[str, Any]:
    """Return session metadata and conversation history."""
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")
    session = _chat_engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    info = session.to_dict()
    info["history"] = [m.to_dict() for m in session.history]
    return info


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    run_server()

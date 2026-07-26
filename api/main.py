"""
New-mir FastAPI Application
============================
Layer 4 — Web interface and REST API.

Endpoints
---------
GET  /                          → Web UI (HTML)
GET  /api/health                → {"status": "ok", "version": "1.2.0"}
POST /api/convert               → Convert uploaded file to binary
POST /api/compress              → Compress raw text/bytes, return bit-string
POST /api/encode-qr             → Encode text to QR-code slot IDs + PNG
GET  /api/encode-qr/{slot_id}   → Retrieve QR PNG by slot_id
POST /api/generate              → Generate code via NeuralCodeGen (RAG-lite context)
GET  /api/memory/stats          → HoneycombMemory pool statistics
GET  /api/compression/estimate  → Compression ratio estimate for sample data
POST /api/train                 → Train model on one or more uploaded files
GET  /api/train/stats           → Global training / memory stats
POST /api/weights/save          → Persist weights + cells to disk permanently
GET  /api/weights/status        → Check whether saved weights exist on disk
POST /api/chat/session          → Create a new chat session
POST /api/chat/{session_id}     → Send message, stream SSE response
GET  /api/chat/continue/{id}    → Continue a paused session (SSE)
POST /api/chat/stop/{id}        → Stop / pause a running session
GET  /api/chat/sessions         → List all active sessions
GET  /api/chat/session/{id}     → Get session info + history
GET  /api/project/tree          → JSON file tree of the project
GET  /api/project/download      → Download full project as ZIP
POST /api/project/upload        → Upload a ZIP archive to replace project files

All endpoints return JSON unless noted otherwise.  File upload endpoints
accept multipart/form-data.  Chat streaming endpoints use text/event-stream.

Persistence
-----------
Trained weights and memory cells are stored in ``data/weights/``:

  data/weights/neural_core.json   — NeuralCodeGen transformer weights
  data/weights/cells.json         — HoneycombMemory cells (all shards merged)

These files are written atomically (tmp → rename) so a crash mid-write never
corrupts the stored data.  On startup the files are loaded automatically if
they exist, so training state survives container restarts.

RAG-lite context enrichment
----------------------------
When generating code the engine searches the cell pool for cells whose
metadata or payload contains tokens from the user's prompt.  Up to 3 matching
cells are decoded and prepended to the prompt as a ``# Context:`` comment
block.  This lets trained knowledge influence generation even from the tiny
nano model.

Streaming implementation note
------------------------------
The chat SSE endpoints use a threading.Queue bridge:

  1. The synchronous ChatEngine generator runs in a daemon thread.
  2. Each SSE chunk is put() into a Queue as it's produced.
  3. The async generator get()s chunks via run_in_executor so the event
     loop is never blocked.

This ensures the browser receives tokens one at a time, and the Stop button
works by setting the session's threading.Event between chunks.
"""

from __future__ import annotations

import asyncio
import base64
import io
import logging
import os
import queue
import threading
import zipfile
from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from api.converters import convert_to_binary
from core.binary_engine import BinaryCompressionEngine
from core.cell_memory import HoneycombMemory
from core.chat_engine import ChatEngine
from core.gpt2_backend import GPT2Backend
from core.neural_core import NeuralCodeGen
from core.qr_encoder import QRBinaryEncoder
from core.background_trainer import BackgroundTrainer
from core.distillation import DEFAULT_DISTILL_PROMPTS, DistillationResult, run_distillation
from core.seed_trainer import run_seed_training
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
# Persistence paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parent.parent

# In Docker, NEW_MIR_STATE_DIR points to a named volume (new_mir_state)
# so weights and stats survive image rebuilds.
# In dev the variable is unset and files land in data/ as before.
_STATE_DIR = Path(os.environ.get("NEW_MIR_STATE_DIR", str(_REPO_ROOT / "data")))
_WEIGHTS_DIR = _STATE_DIR / "weights"
_WEIGHTS_FILE = _WEIGHTS_DIR / "neural_core.json"
_CELLS_FILE = _WEIGHTS_DIR / "cells.json"

# ---------------------------------------------------------------------------
# Application state (singletons initialised at startup)
# ---------------------------------------------------------------------------

_memory = HoneycombMemory(capacity=65_536)
_memory_shards: list[HoneycombMemory] = [_memory]
_qr_encoder = QRBinaryEncoder()
_compression_engine = BinaryCompressionEngine()

# Nano NeuralCodeGen — used for the Code Gen and Training tabs
_neural_gen = NeuralCodeGen()

# GPT-2 backend — used exclusively for the Chat tab
# Model name can be overridden via NEW_MIR_CHAT_MODEL env var, e.g.:
#   NEW_MIR_CHAT_MODEL=gpt2-medium
#   NEW_MIR_CHAT_MODEL=sberbank-ai/rugpt3small   (Russian)
#   NEW_MIR_CHAT_MODEL=bigscience/bloom-560m     (46 languages)
_gpt2_gen = GPT2Backend()

_trainer: HoneycombTrainer | None = None
_chat_engine: ChatEngine | None = None
_bg_trainer: BackgroundTrainer | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown logic."""
    global _trainer, _chat_engine, _bg_trainer
    logger.info("Starting New-mir …")
    loop = asyncio.get_event_loop()

    # --- Load nano model weights ----------------------------------------
    # Try file-based persistence first so trained weights survive restarts.
    if _WEIGHTS_FILE.exists():
        try:
            saved = await loop.run_in_executor(
                None, NeuralCodeGen.load_from_file, _WEIGHTS_FILE
            )
            # Copy weights into the singleton without replacing the object
            _neural_gen.weights = saved.weights
            logger.info(
                "NeuralCodeGen weights restored from %s — params: %d",
                _WEIGHTS_FILE,
                _neural_gen.parameter_count,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not load saved weights (%s) — using demo weights", exc)
            await loop.run_in_executor(None, _neural_gen.load_demo_weights)
    else:
        await loop.run_in_executor(None, _neural_gen.load_demo_weights)
        logger.info("NeuralCodeGen (nano) loaded — params: %d", _neural_gen.parameter_count)

    # --- Load saved cells -----------------------------------------------
    if _CELLS_FILE.exists():
        try:
            n = await loop.run_in_executor(None, _memory.load_from_file, _CELLS_FILE)
            logger.info("Restored %d cells from %s", n, _CELLS_FILE)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not load saved cells (%s) — starting empty", exc)

    # --- GPT-2 for chat -------------------------------------------------
    try:
        await loop.run_in_executor(None, _gpt2_gen.load_demo_weights)
        logger.info(
            "GPT-2 '%s' loaded — params: %d",
            _gpt2_gen.model_name,
            _gpt2_gen.parameter_count,
        )
        chat_model: Any = _gpt2_gen
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "GPT-2 load failed (%s) — chat will fall back to nano model", exc
        )
        chat_model = _neural_gen

    _trainer = HoneycombTrainer(
        memory_shards=_memory_shards,
        qr_encoder=_qr_encoder,
        compression_engine=_compression_engine,
        neural_gen=_neural_gen,  # training still uses the nano model
    )
    _chat_engine = ChatEngine(neural_gen=chat_model)
    logger.info("HoneycombTrainer and ChatEngine ready.")

    # Auto-train on seed data (Russian, Rust, multilingual, Python) on first startup.
    # Skipped automatically if already done (flag in data/training_stats.json).
    try:
        await loop.run_in_executor(None, run_seed_training, _trainer)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Seed training skipped: %s", exc)

    # Auto-save weights after seed training so that trained state survives
    # container rebuilds (docker compose up -d --build).  Without this step
    # the fine-tuned weights live only in RAM and are lost on every restart.
    if _neural_gen.weights is not None:
        try:
            _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
            await loop.run_in_executor(None, _neural_gen.save_to_file, _WEIGHTS_FILE)
            await loop.run_in_executor(None, _memory.save_to_file, _CELLS_FILE)
            logger.info(
                "Weights auto-saved to %s (%d bytes)",
                _WEIGHTS_FILE,
                _WEIGHTS_FILE.stat().st_size,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Auto-save weights failed: %s", exc)

    # --- Start background distillation scheduler ----------------------------
    # Runs in a daemon thread: every 30 min GPT-2 generates new examples,
    # mixes them with old ones from the replay buffer, and fine-tunes the
    # nano model — all while the server is handling requests normally.
    def _sync_save_weights() -> None:
        """Synchronous weight-save helper passed to BackgroundTrainer."""
        if _neural_gen.weights is not None:
            _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
            _neural_gen.save_to_file(_WEIGHTS_FILE)
            _memory.save_to_file(_CELLS_FILE)

    _bg_trainer = BackgroundTrainer(
        teacher=_gpt2_gen,
        student=_neural_gen,
        save_fn=_sync_save_weights,
        interval_seconds=int(os.environ.get("NEW_MIR_DISTILL_INTERVAL", "1800")),
        new_per_cycle=int(os.environ.get("NEW_MIR_DISTILL_NEW", "5")),
        replay_per_cycle=int(os.environ.get("NEW_MIR_DISTILL_REPLAY", "10")),
    )
    _bg_trainer.start()

    yield

    # --- Shutdown -----------------------------------------------------------
    if _bg_trainer is not None:
        _bg_trainer.stop()
    logger.info("New-mir shutting down.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="New-mir Neural Code Engine",
    description=(
        "Honeycomb-memory neural architecture for code generation. "
        "Stores data as QR-code binary slots, compresses everything with "
        "multi-algorithm pipeline, generates code via numpy Transformer, "
        "and chats via GPT-2."
    ),
    version="1.2.0",
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
        "version": "1.2.0",
        "memory_cells": _memory.size,
        "qr_slots": _qr_encoder.slot_count,
        "model_params": _neural_gen.parameter_count,
        "chat_model": _gpt2_gen.model_name,
        "chat_model_params": _gpt2_gen.parameter_count,
        "chat_model_loaded": _gpt2_gen.weights is not None,
        "weights_saved_on_disk": _WEIGHTS_FILE.exists(),
        "cells_saved_on_disk": _CELLS_FILE.exists(),
        "trainer": trainer_stats,
    }


# ---------------------------------------------------------------------------
# Weights persistence
# ---------------------------------------------------------------------------


@app.post("/api/weights/save", tags=["Persistence"])
async def save_weights() -> dict[str, Any]:
    """Persist current model weights **and** all memory cells to disk.

    Both files are written atomically.  After this call the training state
    will survive container restarts — the next startup will load from disk
    instead of re-initialising with demo weights.

    Returns
    -------
    JSON with paths of the files written and their sizes in bytes.
    """
    if _neural_gen.weights is None:
        raise HTTPException(status_code=503, detail="Model weights not loaded")

    loop = asyncio.get_event_loop()
    _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

    await loop.run_in_executor(None, _neural_gen.save_to_file, _WEIGHTS_FILE)
    await loop.run_in_executor(None, _memory.save_to_file, _CELLS_FILE)

    weights_size = _WEIGHTS_FILE.stat().st_size
    cells_size = _CELLS_FILE.stat().st_size
    logger.info(
        "Weights saved: %d bytes, cells saved: %d bytes",
        weights_size,
        cells_size,
    )
    return {
        "saved": True,
        "weights_file": str(_WEIGHTS_FILE),
        "weights_bytes": weights_size,
        "cells_file": str(_CELLS_FILE),
        "cells_bytes": cells_size,
        "cells_count": _memory.size,
    }


@app.get("/api/weights/status", tags=["Persistence"])
async def weights_status() -> dict[str, Any]:
    """Return whether persisted weight and cell files exist on disk."""
    return {
        "weights_saved": _WEIGHTS_FILE.exists(),
        "weights_bytes": _WEIGHTS_FILE.stat().st_size if _WEIGHTS_FILE.exists() else 0,
        "cells_saved": _CELLS_FILE.exists(),
        "cells_bytes": _CELLS_FILE.stat().st_size if _CELLS_FILE.exists() else 0,
        "cells_in_memory": _memory.size,
    }


# ---------------------------------------------------------------------------
# Knowledge Distillation: GPT-2 → NeuralCodeGen
# ---------------------------------------------------------------------------


@app.post("/api/distill", tags=["Training"])
async def distill(
    max_new_tokens: int = Form(default=128),
    temperature: float = Form(default=0.7),
    epochs: int = Form(default=3),
    prompts: str = Form(default=""),
) -> dict[str, Any]:
    """
    Run GPT-2 → NeuralCodeGen knowledge distillation.

    GPT-2 (teacher) generates text continuations for seed prompts.
    NeuralCodeGen (student) is then fine-tuned on those continuations.
    This transfers knowledge from the large pre-trained GPT-2 model into
    the compact nano model without needing any external dataset.

    Parameters
    ----------
    max_new_tokens : int
        Tokens GPT-2 generates per prompt (default 128).
    temperature : float
        GPT-2 sampling temperature — 0.7 is focused but not repetitive.
    epochs : int
        Fine-tuning epochs on the student per example (default 3).
    prompts : str
        Optional JSON array of custom seed prompts.
        If empty, the built-in 30-prompt set is used.

    Returns
    -------
    JSON DistillationResult summary with loss statistics.
    """
    if _gpt2_gen.weights is None:
        return {"error": "GPT-2 not loaded — cannot distill"}
    if _neural_gen.weights is None:
        return {"error": "NeuralCodeGen not loaded — cannot distill"}

    # Parse optional custom prompts
    custom_prompts: list[str] | None = None
    if prompts.strip():
        import json as _json

        try:
            parsed = _json.loads(prompts)
            if isinstance(parsed, list):
                custom_prompts = [str(p) for p in parsed if p]
        except ValueError:
            return {"error": "prompts must be a JSON array of strings"}

    loop = asyncio.get_event_loop()
    result: DistillationResult = await loop.run_in_executor(
        None,
        lambda: run_distillation(
            teacher=_gpt2_gen,
            student=_neural_gen,
            prompts=custom_prompts,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            epochs=epochs,
        ),
    )

    # Auto-save weights after distillation so the student's progress persists.
    if _neural_gen.weights is not None and result.examples_generated > 0:
        try:
            _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
            await loop.run_in_executor(None, _neural_gen.save_to_file, _WEIGHTS_FILE)
            await loop.run_in_executor(None, _memory.save_to_file, _CELLS_FILE)
            logger.info(
                "Weights auto-saved after distillation (%d examples)", result.examples_generated
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Auto-save after distillation failed: %s", exc)

    return result.to_dict()


@app.get("/api/distill/status", tags=["Training"])
async def distill_status() -> dict[str, Any]:
    """Return the current status of the background distillation scheduler.

    Shows whether it is running, how many cycles have completed, the replay
    buffer size, and statistics from the last cycle.
    """
    if _bg_trainer is None:
        return {"running": False, "cycles_completed": 0, "buffer_size": 0, "last_cycle": None}
    return _bg_trainer.status()


@app.post("/api/distill/start", tags=["Training"])
async def distill_start(
    interval_seconds: int = Form(default=1800),
) -> dict[str, Any]:
    """Start (or restart) the background distillation scheduler.

    Parameters
    ----------
    interval_seconds : int
        Seconds between distillation cycles (default 1800 = 30 min).
        Set to 300 for every 5 minutes, 3600 for every hour, etc.
    """
    if _bg_trainer is None:
        return {"started": False, "error": "BackgroundTrainer not initialised"}
    if _bg_trainer.is_running:
        return {"started": False, "error": "Already running", "status": _bg_trainer.status()}
    _bg_trainer.interval_seconds = interval_seconds
    _bg_trainer.start()
    return {"started": True, "interval_seconds": interval_seconds}


@app.post("/api/distill/stop", tags=["Training"])
async def distill_stop() -> dict[str, Any]:
    """Stop the background distillation scheduler."""
    if _bg_trainer is None:
        return {"stopped": False, "error": "BackgroundTrainer not initialised"}
    if not _bg_trainer.is_running:
        return {"stopped": False, "error": "Not running"}
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _bg_trainer.stop)
    return {"stopped": True}


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
# Code generation (nano NeuralCodeGen + RAG-lite cell context)
# ---------------------------------------------------------------------------

# Maximum characters from each matching cell to inject as context
_RAG_CELL_CHARS = 256
# Maximum number of cells to inject per prompt
_RAG_MAX_CELLS = 3


def _build_rag_prompt(prompt: str, language: str) -> tuple[str, int]:
    """Search cells for *prompt* tokens and prepend matching snippets.

    Returns
    -------
    (enriched_prompt, cells_used)
    """
    hits = _memory.search_cells(f"{prompt} {language}", limit=_RAG_MAX_CELLS)
    if not hits:
        return prompt, 0

    snippets: list[str] = []
    for cell in hits:
        raw = cell.binary_payload[:_RAG_CELL_CHARS * 4]
        text = raw.decode("utf-8", errors="ignore").strip()
        if text:
            snippets.append(text[:_RAG_CELL_CHARS])

    if not snippets:
        return prompt, 0

    context_block = "# Context from training memory:\n"
    for i, s in enumerate(snippets, 1):
        context_block += f"# [{i}] {s}\n"
    context_block += "#\n"

    return context_block + prompt, len(snippets)


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

    RAG-lite enrichment: before generation the engine searches the in-memory
    cell pool for content related to the prompt.  Up to 3 matching cells are
    injected as a comment block so training history influences output.

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

    # RAG-lite: enrich prompt with relevant cell content
    enriched_prompt, cells_used = await loop.run_in_executor(
        None, _build_rag_prompt, prompt, language
    )

    if description_mode:
        generated = await loop.run_in_executor(
            None,
            lambda: _neural_gen.generate_from_description(
                enriched_prompt,
                language=language,
                max_new_tokens=max_new_tokens,
            ),
        )
    else:
        generated = await loop.run_in_executor(
            None,
            lambda: _neural_gen.generate(
                enriched_prompt,
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
        "tokens_generated": len(generated) - len(enriched_prompt),
        "cells_used_as_context": cells_used,
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

    # Persist weights after every manual training session so progress is
    # not lost on container restart or image rebuild.
    if _neural_gen.weights is not None:
        try:
            _WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
            await loop.run_in_executor(None, _neural_gen.save_to_file, _WEIGHTS_FILE)
            await loop.run_in_executor(None, _memory.save_to_file, _CELLS_FILE)
            logger.info("Weights auto-saved after manual training session %s", session.session_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Auto-save after training failed: %s", exc)

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
# Project explorer — file tree + download + upload
# ---------------------------------------------------------------------------

# Directories / patterns to exclude from the project tree and ZIP export
_EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache"}
_EXCLUDE_EXTS = {".pyc", ".pyo", ".tmp"}


def _build_tree(root: Path, rel: Path | None = None) -> list[dict[str, Any]]:
    """Recursively build a GitHub-style file tree under *root*."""
    base = rel or Path(".")
    items: list[dict[str, Any]] = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return items
    for entry in entries:
        if entry.name in _EXCLUDE_DIRS or entry.suffix in _EXCLUDE_EXTS:
            continue
        node: dict[str, Any] = {"name": entry.name, "path": str(base / entry.name)}
        if entry.is_dir():
            node["type"] = "dir"
            node["children"] = _build_tree(entry, base / entry.name)
        else:
            node["type"] = "file"
            node["size"] = entry.stat().st_size
        items.append(node)
    return items


@app.get("/api/project/tree", tags=["Project"])
async def project_tree() -> dict[str, Any]:
    """Return a recursive JSON file tree of the project repository."""
    loop = asyncio.get_event_loop()
    tree = await loop.run_in_executor(None, _build_tree, _REPO_ROOT)
    return {"root": str(_REPO_ROOT.name), "tree": tree}


@app.get("/api/project/download", tags=["Project"])
async def project_download() -> Response:
    """Stream the entire project as a ZIP archive (excludes .git / __pycache__)."""

    def _make_zip() -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(_REPO_ROOT.rglob("*")):
                if path.is_file():
                    # Skip excluded dirs/extensions
                    parts = path.relative_to(_REPO_ROOT).parts
                    if any(p in _EXCLUDE_DIRS for p in parts):
                        continue
                    if path.suffix in _EXCLUDE_EXTS:
                        continue
                    zf.write(path, path.relative_to(_REPO_ROOT))
        return buf.getvalue()

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, _make_zip)
    return Response(
        content=data,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=new-mir.zip"},
    )


@app.post("/api/project/upload", tags=["Project"])
async def project_upload(file: UploadFile) -> dict[str, Any]:
    """Upload a ZIP archive and extract it into the project directory.

    Existing files are overwritten.  Only files inside the archive are
    written; directory traversal (``../``) is blocked.

    Returns
    -------
    JSON with the list of extracted file paths.
    """
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty upload")

    def _extract(data: bytes) -> list[str]:
        extracted: list[str] = []
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                # Block path traversal
                target = (_REPO_ROOT / info.filename).resolve()
                if not str(target).startswith(str(_REPO_ROOT)):
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(info.filename))
                extracted.append(str(Path(info.filename)))
        return extracted

    loop = asyncio.get_event_loop()
    extracted = await loop.run_in_executor(None, _extract, raw)
    return {"extracted": extracted, "count": len(extracted)}


# ---------------------------------------------------------------------------
# Chat — SSE streaming dialogue
# ---------------------------------------------------------------------------
#
# STREAMING FIX:
# The previous implementation used:
#
#   for chunk in await loop.run_in_executor(None, list, _sync_gen()):
#       yield chunk
#
# This collected ALL tokens into a list before sending the first byte,
# making Stop/Continue completely non-functional.  The corrected version
# uses a threading.Queue bridge: the generator thread puts() chunks as
# they're produced, and the async generator gets() them one at a time
# via run_in_executor without ever blocking the event loop.
# ---------------------------------------------------------------------------

_SSE_QUEUE_MAXSIZE = 256  # max buffered chunks per stream


def _stream_via_queue(
    sync_gen_fn: Iterator[str],
    loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[str, None]:
    """
    Bridge a synchronous SSE generator to an async one using a Queue.

    The generator runs in a daemon thread; the async generator yields
    chunks as they arrive, preserving true token-by-token streaming.
    """
    q: queue.Queue[str | None] = queue.Queue(maxsize=_SSE_QUEUE_MAXSIZE)

    def _producer() -> None:
        try:
            for chunk in sync_gen_fn:
                q.put(chunk)
        except Exception:  # noqa: BLE001,S110
            pass
        finally:
            q.put(None)  # sentinel: generation finished

    thread = threading.Thread(target=_producer, daemon=True)
    thread.start()

    async def _consumer() -> AsyncGenerator[str, None]:
        while True:
            chunk = await loop.run_in_executor(None, q.get)
            if chunk is None:
                break
            yield chunk
        thread.join(timeout=5.0)

    return _consumer()


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

    Tokens are streamed one chunk at a time (not buffered), so the Stop
    button interrupts generation at the next chunk boundary.
    """
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")

    session = _chat_engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")

    loop = asyncio.get_event_loop()

    sync_gen = _chat_engine.generate_stream(
        session_id=session_id,
        user_message=message,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return StreamingResponse(
        _stream_via_queue(sync_gen, loop),
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
    Tokens are streamed in real-time; pressing Stop pauses again.
    """
    if _chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not ready")

    loop = asyncio.get_event_loop()

    sync_gen = _chat_engine.continue_stream(
        session_id=session_id,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return StreamingResponse(
        _stream_via_queue(sync_gen, loop),
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
# Hardware Analysis & Auto-Optimization
# ---------------------------------------------------------------------------

# Runtime-adjustable inference settings (modified by /api/hardware/optimize).
# Workers share memory in a single-process dev setup; in multi-worker prod
# the values are per-process which is fine — each worker self-optimises.
_hw_throttle_ms: int = 1
_hw_max_tokens: int = 4096


def _collect_hardware() -> dict[str, Any]:
    """Collect CPU / RAM / disk metrics using only stdlib (no psutil)."""
    import platform
    import shutil

    info: dict[str, Any] = {}

    # ── Platform ──────────────────────────────────────────────────────────
    info["platform"] = platform.system()
    info["platform_release"] = platform.release()
    info["python_version"] = platform.python_version()
    info["machine"] = platform.machine()

    # ── CPU ───────────────────────────────────────────────────────────────
    cpu_count = os.cpu_count() or 1
    info["cpu_count"] = cpu_count

    # CPU model name (Linux /proc/cpuinfo)
    cpu_model = platform.processor() or "Unknown"
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as fh:
            for line in fh:
                if "model name" in line:
                    cpu_model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    info["cpu_model"] = cpu_model[:72]

    # Load average (POSIX only; Windows falls back to 0)
    try:
        load1, load5, load15 = os.getloadavg()
    except AttributeError:
        load1 = load5 = load15 = 0.0
    info["cpu_load_1m"] = round(load1, 2)
    info["cpu_load_5m"] = round(load5, 2)
    info["cpu_load_15m"] = round(load15, 2)
    info["cpu_load_pct"] = round(load1 / cpu_count * 100, 1)

    # ── RAM ───────────────────────────────────────────────────────────────
    ram_total_mb = ram_avail_mb = 0
    try:
        mem: dict[str, int] = {}
        with open("/proc/meminfo", encoding="utf-8") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(":")] = int(parts[1])
        ram_total_mb = mem.get("MemTotal", 0) // 1024
        ram_avail_mb = mem.get("MemAvailable", 0) // 1024
    except OSError:
        pass
    info["ram_total_mb"] = ram_total_mb
    info["ram_available_mb"] = ram_avail_mb
    info["ram_used_mb"] = max(ram_total_mb - ram_avail_mb, 0)
    info["ram_used_pct"] = (
        round((ram_total_mb - ram_avail_mb) / max(ram_total_mb, 1) * 100, 1)
        if ram_total_mb
        else 0.0
    )

    # ── Disk ──────────────────────────────────────────────────────────────
    try:
        du = shutil.disk_usage("/")
        info["disk_total_gb"] = round(du.total / 1e9, 1)
        info["disk_used_gb"] = round(du.used / 1e9, 1)
        info["disk_free_gb"] = round(du.free / 1e9, 1)
        info["disk_used_pct"] = round(du.used / max(du.total, 1) * 100, 1)
    except OSError:
        info["disk_total_gb"] = info["disk_used_gb"] = info["disk_free_gb"] = 0.0
        info["disk_used_pct"] = 0.0

    # ── Container limits (cgroup v2) ──────────────────────────────────────
    mem_limit_mb = 0
    try:
        with open("/sys/fs/cgroup/memory.max", encoding="utf-8") as fh:
            val = fh.read().strip()
            if val != "max":
                mem_limit_mb = int(val) // (1024 * 1024)
    except OSError:
        pass
    info["container_mem_limit_mb"] = mem_limit_mb  # 0 = no limit

    # ── Current model state ───────────────────────────────────────────────
    info["model_params"] = _neural_gen.parameter_count
    info["model_max_seq"] = _neural_gen._max_seq
    info["model_embed_dim"] = _neural_gen._embed_dim
    info["gpt2_model"] = _gpt2_gen.model_name
    info["gpt2_params"] = _gpt2_gen.parameter_count
    info["current_throttle_ms"] = _hw_throttle_ms
    info["current_max_tokens"] = _hw_max_tokens

    # ── Safety recommendation ─────────────────────────────────────────────
    load_pct = info["cpu_load_pct"]
    avail_mb = info["ram_available_mb"]
    disk_pct = info["disk_used_pct"]

    if load_pct > 80 or avail_mb < 150 or disk_pct > 95:
        mode = "safe"
        rec_throttle = 15
        rec_tokens = 128
        rec_seq = 128
        status = "Критическая нагрузка — безопасный режим"
        status_level = "critical"
    elif load_pct > 55 or avail_mb < 400 or disk_pct > 85:
        mode = "balanced"
        rec_throttle = 5
        rec_tokens = 512
        rec_seq = 256
        status = "Умеренная нагрузка — сбалансированный режим"
        status_level = "warn"
    else:
        mode = "performance"
        rec_throttle = 1
        rec_tokens = 4096
        rec_seq = 512
        status = "Нагрузка в норме — режим максимальной производительности"
        status_level = "ok"

    info["safety_mode"] = mode
    info["status"] = status
    info["status_level"] = status_level
    info["recommended_throttle_ms"] = rec_throttle
    info["recommended_max_tokens"] = rec_tokens
    info["recommended_max_seq"] = rec_seq

    return info


@app.get("/api/hardware", tags=["System"])
async def hardware_info() -> dict[str, Any]:
    """
    Return CPU, RAM, disk metrics plus a safety-mode recommendation.

    The recommendation picks one of three modes based on current load:

    * **performance** — CPU ≤ 55 %, RAM free ≥ 400 MB, disk ≤ 85 %
    * **balanced**    — moderate load
    * **safe**        — CPU > 80 %, RAM free < 150 MB, or disk > 95 %

    Call ``POST /api/hardware/optimize`` to apply the recommendation.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _collect_hardware)


@app.post("/api/hardware/optimize", tags=["System"])
async def hardware_optimize() -> dict[str, Any]:
    """
    Apply the hardware-based safety recommendation in-process.

    Adjusts:
    * ``_hw_throttle_ms``     — sleep between token batches (limits CPU)
    * ``_hw_max_tokens``      — default chat / generate token budget
    * ``_neural_gen._max_seq`` — NeuralCodeGen context window (limits RAM)

    Returns the new settings and a human-readable status message.
    """
    global _hw_throttle_ms, _hw_max_tokens

    loop = asyncio.get_event_loop()
    hw = await loop.run_in_executor(None, _collect_hardware)

    _hw_throttle_ms = hw["recommended_throttle_ms"]
    _hw_max_tokens = hw["recommended_max_tokens"]
    _neural_gen._max_seq = hw["recommended_max_seq"]

    logger.info(
        "Hardware optimisation applied: mode=%s throttle=%dms max_tokens=%d max_seq=%d",
        hw["safety_mode"],
        _hw_throttle_ms,
        _hw_max_tokens,
        _neural_gen._max_seq,
    )

    return {
        "optimised": True,
        "mode": hw["safety_mode"],
        "status": hw["status"],
        "status_level": hw["status_level"],
        "throttle_ms": _hw_throttle_ms,
        "max_tokens": _hw_max_tokens,
        "max_seq": _neural_gen._max_seq,
        "cpu_load_pct": hw["cpu_load_pct"],
        "ram_available_mb": hw["ram_available_mb"],
        "disk_used_pct": hw["disk_used_pct"],
    }


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


if __name__ == "__main__":
    run_server()

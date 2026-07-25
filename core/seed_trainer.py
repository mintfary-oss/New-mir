"""Seed Trainer
==============
Loads built-in seed data (Russian, Rust, multilingual, Python examples,
Pulumi) and trains the honeycomb memory on startup for any files that have
not yet been trained.

The seed data lives in ``data/seed/`` relative to the repository root.

Per-file tracking (no manual flag resets needed)
-------------------------------------------------
Instead of a single ``seed_loaded`` boolean, we store a list of filenames
that have already been trained in ``data/training_stats.json``::

    {
      "seed_trained_files": ["russian_intro.txt", "multilingual.txt", ...],
      ...
    }

On every startup the trainer computes::

    pending = set(SEED_FILES) - set(seed_trained_files)

Only files in *pending* are trained.  This means:

* Adding a new file to ``SEED_FILES`` automatically triggers training on
  the next restart — no manual flag reset required.
* Existing files are never re-trained unless the tracking entry is removed.
* Old deployments that have ``seed_loaded: true`` but no
  ``seed_trained_files`` are treated as having trained all current files
  (backward-compatible upgrade path).
"""

from __future__ import annotations

import fcntl
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.trainer import HoneycombTrainer

logger = logging.getLogger("new-mir.seed_trainer")

_REPO_ROOT = Path(__file__).parent.parent
_SEED_DIR = _REPO_ROOT / "data" / "seed"

# Persistent state directory.
# In Docker, NEW_MIR_STATE_DIR points to a named volume so
# training_stats.json survives image rebuilds.
# In dev the variable is unset and the file lands in data/ as before.
_STATE_DIR = Path(os.environ.get("NEW_MIR_STATE_DIR", str(_REPO_ROOT / "data")))
_STATS_FILE = _STATE_DIR / "training_stats.json"

# Master list of seed files shipped with the repository.
# Simply add a new filename here to have it trained automatically on next start.
SEED_FILES = [
    "russian_intro.txt",
    "multilingual.txt",
    "python_examples.py",
    "rust_basics.rs",
    "pulumi_capabilities.txt",
    # Kimi-K2 by Moonshot AI — MoE architecture, deployment, tool-call guidance
    "kimi_k2_readme.md",
    "kimi_k2_deploy.md",
    "kimi_k2_tools.md",
    # OpenAI Cookbook — prompting, reliability techniques, LLM best practices
    "openai_cookbook.md",
]

# Files that existed *before* per-file tracking was introduced (v1.0 / v1.1).
# Used only for backward-compat migration: if an old installation has
# ``seed_loaded: True`` but no ``seed_trained_files`` list, we assume
# exactly these four files were already trained and nothing more.
_LEGACY_SEED_FILES = [
    "russian_intro.txt",
    "multilingual.txt",
    "python_examples.py",
    "rust_basics.rs",
]


# ---------------------------------------------------------------------------
# Stats persistence helpers
# ---------------------------------------------------------------------------

def _load_stats() -> dict[str, object]:
    """Load ``data/training_stats.json``; return a safe default on any error."""
    try:
        if _STATS_FILE.exists():
            with _STATS_FILE.open(encoding="utf-8") as fh:
                return json.load(fh)
    except Exception:  # noqa: BLE001,S110
        pass
    return {
        "sessions": [],
        "total_files_ever": 0,
        "total_cells_ever": 0,
        # Legacy boolean flag (kept for backward compat reads)
        "seed_loaded": False,
        "seed_loaded_at": None,
        # Per-file tracking (new)
        "seed_trained_files": [],
    }


def _save_stats(stats: dict[str, object]) -> None:
    try:
        _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _STATS_FILE.open("w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not save training_stats.json: %s", exc)


def _get_trained_files(stats: dict[str, object]) -> set[str]:
    """Return the set of filenames that have already been trained.

    Handles backward compatibility:
    * New format → read ``seed_trained_files`` list directly.
    * Old format (``seed_loaded: True``, no ``seed_trained_files``) →
      treat only the original legacy files as trained so that any newly
      added seed files (e.g. ``pulumi_capabilities.txt``) are detected
      as pending and trained automatically on the next restart.
    """
    raw = stats.get("seed_trained_files")
    if isinstance(raw, list) and raw:
        return set(raw)
    # Backward compat: old boolean flag was True → only the legacy 4 files
    # were trained; anything added later is still pending.
    if stats.get("seed_loaded"):
        return set(_LEGACY_SEED_FILES)
    return set()


def _mark_files_trained(filenames: list[str]) -> None:
    """Append *filenames* to the trained-files list and persist."""
    stats = _load_stats()
    trained: set[str] = _get_trained_files(stats)
    trained.update(filenames)
    stats["seed_trained_files"] = sorted(trained)
    # Keep legacy flag in sync for external tooling that may read it
    stats["seed_loaded"] = True
    stats["seed_loaded_at"] = datetime.now(tz=timezone.utc).isoformat()
    _save_stats(stats)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def pending_seed_files() -> list[str]:
    """Return seed filenames that exist on disk but have not been trained yet."""
    trained = _get_trained_files(_load_stats())
    pending: list[str] = []
    for fname in SEED_FILES:
        if fname not in trained and (_SEED_DIR / fname).exists():
            pending.append(fname)
    return pending


def load_seed_data(filenames: list[str]) -> list[tuple[str, bytes]]:
    """Read *filenames* from ``data/seed/`` and return (name, bytes) pairs."""
    pairs: list[tuple[str, bytes]] = []
    for fname in filenames:
        path = _SEED_DIR / fname
        if not path.exists():
            logger.warning("Seed file not found, skipping: %s", path)
            continue
        try:
            data = path.read_bytes()
            pairs.append((fname, data))
            logger.info("Loaded seed file: %s (%d bytes)", fname, len(data))
        except OSError as exc:
            logger.warning("Could not read seed file %s: %s", path, exc)
    return pairs


def run_seed_training(trainer: HoneycombTrainer) -> None:
    """Train on any seed files that have not been trained yet.

    Called automatically at startup.  Adding a new filename to
    ``SEED_FILES`` is all that is needed to trigger training on the
    next restart — no manual flag resets required.

    Multi-worker safety
    -------------------
    When uvicorn runs with ``workers > 1`` every worker process calls this
    function during its own ``lifespan`` startup.  Without a lock they all
    read ``training_stats.json`` simultaneously (before any of them has
    written it), detect the same pending files, and run duplicate training
    sessions.

    A non-blocking exclusive file lock (``fcntl.LOCK_EX | LOCK_NB``) ensures
    that exactly one worker proceeds; all others detect the held lock and
    return immediately.  The winning worker releases the lock after it has
    persisted the updated ``training_stats.json``, so a later restart will
    find an up-to-date file and skip training entirely.
    """
    from core.trainer import HoneycombTrainer  # runtime isinstance check

    if not isinstance(trainer, HoneycombTrainer):
        logger.error(
            "run_seed_training: expected HoneycombTrainer, got %s", type(trainer)
        )
        return

    # ------------------------------------------------------------------ #
    # Acquire an exclusive non-blocking file lock.                         #
    # Workers that cannot acquire the lock skip — the winning worker will  #
    # update training_stats.json, so they won't see pending files next     #
    # time around.                                                          #
    # ------------------------------------------------------------------ #
    _lock_path = _STATE_DIR / "seed_training.lock"
    try:
        _lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_fh = _lock_path.open("w")
        fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (BlockingIOError, OSError):
        # Another worker holds the lock — let it handle training.
        logger.info(
            "Seed training already in progress in another worker — skipping."
        )
        lock_fh.close()
        return

    try:
        pending = pending_seed_files()
        if not pending:
            trained = _get_trained_files(_load_stats())
            logger.info(
                "Seed data already up to date — %d file(s) trained, none pending.",
                len(trained),
            )
            return

        logger.info(
            "New seed file(s) detected: %s — starting training…",
            ", ".join(pending),
        )
        pairs = load_seed_data(pending)
        if not pairs:
            logger.warning("No seed files could be read — seed training skipped.")
            return

        try:
            session = trainer.train_files(pairs)
            trained_names = [str(f["filename"]) for f in session.accepted_files]
            logger.info(
                "Seed training complete: %d files, %d cells, %.2fs",
                len(trained_names),
                len(session.cells_written),
                session.duration_s,
            )
            _mark_files_trained(trained_names)
        except Exception as exc:  # noqa: BLE001
            logger.error("Seed training failed: %s", exc)
    finally:
        fcntl.flock(lock_fh, fcntl.LOCK_UN)
        lock_fh.close()

"""Seed Trainer
==============
Loads built-in seed data (Russian, Rust, multilingual, Python examples)
and trains the honeycomb memory on startup when seed has not been loaded yet.

The seed data lives in ``data/seed/`` relative to the repository root.
After a successful seed run the flag ``seed_loaded`` is written to
``data/training_stats.json`` so subsequent restarts skip re-training.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.trainer import HoneycombTrainer

logger = logging.getLogger("new-mir.seed_trainer")

_REPO_ROOT = Path(__file__).parent.parent
_SEED_DIR = _REPO_ROOT / "data" / "seed"
_STATS_FILE = _REPO_ROOT / "data" / "training_stats.json"

SEED_FILES = [
    "russian_intro.txt",
    "multilingual.txt",
    "python_examples.py",
    "rust_basics.rs",
    "pulumi_capabilities.txt",
]


def _load_stats() -> dict[str, object]:
    try:
        if _STATS_FILE.exists():
            with _STATS_FILE.open(encoding="utf-8") as fh:
                return json.load(fh)
    except Exception:  # noqa: BLE001,S110
        pass
    return {"sessions": [], "total_files_ever": 0, "total_cells_ever": 0,
            "seed_loaded": False, "seed_loaded_at": None}


def _save_stats(stats: dict[str, object]) -> None:
    try:
        _STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _STATS_FILE.open("w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not save training_stats.json: %s", exc)


def is_seed_loaded() -> bool:
    return bool(_load_stats().get("seed_loaded", False))


def mark_seed_loaded() -> None:
    stats = _load_stats()
    stats["seed_loaded"] = True
    stats["seed_loaded_at"] = datetime.now(tz=timezone.utc).isoformat()
    _save_stats(stats)


def load_seed_data() -> list[tuple[str, bytes]]:
    pairs: list[tuple[str, bytes]] = []
    for fname in SEED_FILES:
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
    """
    Train on seed data using *trainer* (HoneycombTrainer instance).
    No-op if seed has already been loaded.
    """
    from core.trainer import HoneycombTrainer  # runtime isinstance check

    if not isinstance(trainer, HoneycombTrainer):
        logger.error("run_seed_training: expected HoneycombTrainer, got %s", type(trainer))
        return

    if is_seed_loaded():
        logger.info("Seed data already loaded — skipping seed training.")
        return

    pairs = load_seed_data()
    if not pairs:
        logger.warning("No seed files found in %s — seed training skipped.", _SEED_DIR)
        return

    logger.info("Starting seed training on %d files…", len(pairs))
    try:
        session = trainer.train_files(pairs)
        logger.info(
            "Seed training complete: %d files, %d cells, %.2fs",
            len(session.accepted_files),
            len(session.cells_written),
            session.duration_s,
        )
        mark_seed_loaded()
    except Exception as exc:  # noqa: BLE001
        logger.error("Seed training failed: %s", exc)

"""Seed Trainer
==============
Loads built-in seed data (Russian, Rust, multilingual, Python examples)
and trains the honeycomb memory on startup when seed has not been loaded yet.

The seed data lives in ``data/seed/`` relative to the repository root.
After a successful seed run the flag ``seed_loaded`` is written to
``data/training_stats.json`` so subsequent restarts skip the seed phase.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("new-mir.seed_trainer")

# Repository root
_REPO_ROOT = Path(__file__).parent.parent
_SEED_DIR = _REPO_ROOT / "data" / "seed"

# Ordered list of seed files to load (filename relative to _SEED_DIR)
SEED_FILES = [
    "russian_intro.txt",
    "multilingual.txt",
    "python_examples.py",
    "rust_basics.rs",
]


def is_seed_loaded() -> bool:
    """Return True if seed data has already been loaded (flag in JSON)."""
    from core.trainer import _load_persistent_stats  # avoid circular import at module level

    stats = _load_persistent_stats()
    return bool(stats.get("seed_loaded", False))


def load_seed_data() -> list[tuple[str, bytes]]:
    """
    Read all seed files from ``data/seed/`` and return (filename, bytes) pairs.

    Missing files are skipped with a warning rather than crashing startup.
    """
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


def run_seed_training(trainer: "object") -> None:
    """
    Run the seed training pass using *trainer* (a HoneycombTrainer instance).

    This function is safe to call multiple times — it is a no-op when the
    seed has already been loaded according to ``training_stats.json``.

    Parameters
    ----------
    trainer :
        A ``core.trainer.HoneycombTrainer`` instance (typed as object to
        avoid a circular import at module level).
    """
    # Inline import to avoid circular dependency
    from core.trainer import HoneycombTrainer, mark_seed_loaded  # noqa: PLC0415

    if not isinstance(trainer, HoneycombTrainer):
        logger.error("run_seed_training: expected HoneycombTrainer, got %s", type(trainer))
        return

    if is_seed_loaded():
        logger.info("Seed data already loaded — skipping seed training pass.")
        return

    pairs = load_seed_data()
    if not pairs:
        logger.warning("No seed files found in %s — seed training skipped.", _SEED_DIR)
        return

    logger.info("Starting seed training on %d files…", len(pairs))
    try:
        session = trainer.train_files(pairs)
        logger.info(
            "Seed training complete: %d files, %d cells written, %.2fs",
            len(session.accepted_files),
            len(session.cells_written),
            session.duration_s,
        )
        mark_seed_loaded()
    except Exception as exc:  # noqa: BLE001
        logger.error("Seed training failed: %s", exc)

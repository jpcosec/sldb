"""Where a store's write journal lives: one YAML file per entry under `.sldb/runtime/journal`."""

from __future__ import annotations

from pathlib import Path

from sldb.store.layout import runtime_dir


def journal_dir(store_path: Path) -> Path:
    """The directory holding a store's journal entries."""
    return runtime_dir(store_path) / "journal"


def journal_entry_path(store_path: Path, seq: int) -> Path:
    """The zero-padded file of one journal entry, whose name is its chain position."""
    return journal_dir(store_path) / f"{seq:010d}.yaml"


def journal_lock_path(store_path: Path) -> Path:
    """The advisory lock serializing journal appends, separate from the store index lock."""
    return runtime_dir(store_path) / "locks" / "journal.lock"

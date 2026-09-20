"""Append one entry to a store's journal, chained to the previous entry.

A journal grows unbounded: nobody rotates or truncates it today, so a store with many
writes keeps one small YAML file per write under `.sldb/runtime/journal/`. The read path
streams by sequence number, so an old, long journal stays cheap to verify; the cost to
watch is directory size and the per-write `max(seq)` scan. Setting `SLDB_JOURNAL_OFF=1`
disables appends, for the write-cost benchmark and for callers that need no history.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sldb.store.io.utils import StoreIOUtils, yaml_dump, yaml_load
from sldb.store.journal.entry import JournalEntry
from sldb.store.journal.hashing import hash_entry_fields
from sldb.store.journal.layout import journal_dir, journal_entry_path
from sldb.store.journal.lock import journal_lock


def append_entry(store_path: Path, data: dict[str, Any]) -> JournalEntry | None:
    """Record one write, chained to the journal's previous entry, under the journal lock."""
    if os.environ.get("SLDB_JOURNAL_OFF"):
        return None
    with journal_lock(store_path):
        return _append_locked(store_path, data)


def _append_locked(store_path: Path, data: dict[str, Any]) -> JournalEntry:
    seq = _next_seq(store_path)
    previous = _read_entry(store_path, seq - 1) if seq > 0 else None
    entry = JournalEntry(**{**data, "previous_hash": previous.entry_hash if previous else None})
    entry.entry_hash = hash_entry_fields(entry.model_dump(exclude={"entry_hash"}))
    StoreIOUtils._atomic_write(journal_entry_path(store_path, seq), yaml_dump(entry.model_dump()))
    return entry


def _next_seq(store_path: Path) -> int:
    d = journal_dir(store_path)
    if not d.is_dir():
        return 0
    return max((int(p.stem) for p in d.glob("*.yaml")), default=-1) + 1


def _read_entry(store_path: Path, seq: int) -> JournalEntry | None:
    path = journal_entry_path(store_path, seq)
    if not path.exists():
        return None
    return JournalEntry(**(yaml_load(path.read_text(encoding="utf-8")) or {}))

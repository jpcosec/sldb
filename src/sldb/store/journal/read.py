"""Read a store's journal, newest first, with optional limit/since/address filters."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sldb.store.io.utils import yaml_load
from sldb.store.journal.entry import JournalEntry
from sldb.store.journal.layout import journal_dir


def read_entries(store_path: Path, limit: int | None = None, since: datetime | None = None, address: str | None = None) -> list[JournalEntry]:
    """Newest-first entries; `since` and `address` narrow the result before `limit` cuts it."""
    entries = _load_newest_first(store_path)
    if since is not None:
        entries = [e for e in entries if _at_or_after(e.timestamp, since)]
    if address is not None:
        entries = [e for e in entries if e.address == address]
    return entries[:limit] if limit is not None else entries


def _load_newest_first(store_path: Path) -> list[JournalEntry]:
    d = journal_dir(store_path)
    if not d.is_dir():
        return []
    return [JournalEntry(**(yaml_load(p.read_text(encoding="utf-8")) or {})) for p in sorted(d.glob("*.yaml"), reverse=True)]


def _at_or_after(timestamp: datetime, since: datetime) -> bool:
    """Compare two timestamps, treating a naive one as UTC rather than raising."""
    stamp = timestamp if timestamp.tzinfo else timestamp.replace(tzinfo=timezone.utc)
    floor = since if since.tzinfo else since.replace(tzinfo=timezone.utc)
    return stamp >= floor

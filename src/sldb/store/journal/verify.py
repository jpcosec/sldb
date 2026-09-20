"""Verify a store journal's hash chain."""

from __future__ import annotations

from pathlib import Path

from sldb.store.io.utils import yaml_load
from sldb.store.journal.entry import JournalEntry
from sldb.store.journal.hashing import hash_entry_fields
from sldb.store.journal.layout import journal_dir
from sldb.store.journal.report import JournalVerifyReport


def verify_chain(store_path: Path) -> JournalVerifyReport:
    """Walk the journal oldest-first, checking each entry's hash and link to the previous."""
    entries = _load_oldest_first(store_path)
    previous = None
    for seq, entry in entries:
        if entry.entry_hash != hash_entry_fields(entry.model_dump(exclude={"entry_hash"})):
            return _report(store_path, entries, seq, "entry_hash mismatch")
        if entry.previous_hash != previous:
            return _report(store_path, entries, seq, "previous_hash mismatch")
        previous = entry.entry_hash
    return _report(store_path, entries, None, None)


def _load_oldest_first(store_path: Path) -> list[tuple[int, JournalEntry]]:
    d = journal_dir(store_path)
    if not d.is_dir():
        return []
    return [(int(p.stem), JournalEntry(**(yaml_load(p.read_text(encoding="utf-8")) or {}))) for p in sorted(d.glob("*.yaml"))]


def _report(store_path: Path, entries: list, broken_seq: int | None, reason: str | None) -> JournalVerifyReport:
    return JournalVerifyReport(
        store=str(store_path), entries=len(entries),
        valid=broken_seq is None, broken_seq=broken_seq, reason=reason,
    )

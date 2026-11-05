"""The write journal, retired on 2026-11-04: the store's past is read from git.

`.sldb/` is versioned whole (docs/architecture/journal-authority.md), so `git log` over its
shards and `sldb docs history <doc>` answer what the journal used to: who wrote what, and when.
The readers stay, answering empty, so that callers importing them keep working; no write
produces a journal any more, and `sldb stores migrate-layout` deletes the one a store had.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.io.shards import load_document_shard
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.layout import documents_shard_path

RETIRED_NOTICE = "El journal fue retirado el 2026-11-04; el pasado del store se consulta con sldb docs history <doc>."


def journal(store: str | Path | None = None, limit: int | None = None, since: datetime | None = None, address: str | None = None) -> list[JournalEntry]:
    """No entries: the journal was retired (see `RETIRED_NOTICE`).

    Args:
        store: The store (path, alias, or None to discover it); still resolved, so an unknown
            store is still an error.
        limit: Ignored.
        since: Ignored.
        address: Ignored.

    Returns:
        An empty list.
    """
    open_store(store, mode="readonly")
    return []


def verify_journal(store: str | Path | None = None) -> JournalVerifyReport:
    """A valid, empty chain: there is no journal to verify any more."""
    location = open_store(store, mode="readonly")
    return JournalVerifyReport(store=str(location.store_path), entries=0, valid=True)


def doc_hashes(store_path: Path, model: str, doc: str) -> tuple[str | None, str | None]:
    """The tracked document's content and field hashes, or (None, None) if untracked."""
    entry = load_document_shard(documents_shard_path(store_path, model, doc))
    return (entry.hash_c, entry.hash_d) if entry else (None, None)

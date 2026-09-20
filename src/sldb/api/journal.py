"""Read a store's write journal and verify its hash chain."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from sldb.api.stores.open_store import open_store
from sldb.store.io import load_store_index
from sldb.store.io.shards import load_document_shard
from sldb.store.journal import JournalEntry, JournalVerifyReport, append_entry, read_entries, verify_chain
from sldb.store.layout import documents_shard_path


def journal(store: str | Path | None = None, limit: int | None = None, since: datetime | None = None, address: str | None = None) -> list[JournalEntry]:
    """Read a store's write journal, newest entry first.

    Args:
        store: The store whose journal to read (path, alias, or None to discover it).
        limit: Return at most this many entries (the newest ones).
        since: Only entries at or after this UTC timestamp.
        address: Only entries for this `Model:doc` address (or model name).

    Returns:
        The matching entries, newest first. An absent journal yields an empty list.
    """
    location = open_store(store, mode="readonly")
    return read_entries(location.store_path, limit=limit, since=since, address=address)


def verify_journal(store: str | Path | None = None) -> JournalVerifyReport:
    """Verify a store journal's hash chain; an absent journal is valid (no history)."""
    location = open_store(store, mode="readonly")
    return verify_chain(location.store_path)


def record(store_path: Path, data: dict[str, Any]) -> JournalEntry:
    """Append one entry to the store's journal."""
    return append_entry(store_path, data)


def store_hash(store_path: Path) -> str:
    """The store's current root hash (`hash_a`)."""
    return load_store_index(store_path).hash_a


def doc_address(model: str, doc: str) -> str:
    """The `Model:doc` address a document journal entry is keyed by."""
    return f"{model}:{doc}"


def doc_hashes(store_path: Path, model: str, doc: str) -> tuple[str | None, str | None]:
    """The tracked document's content and field hashes, or (None, None) if untracked."""
    entry = load_document_shard(documents_shard_path(store_path, model, doc))
    return (entry.hash_c, entry.hash_d) if entry else (None, None)

"""The hashes the store holds for a tracked document."""

from __future__ import annotations

from pathlib import Path

from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path


def doc_hashes(store_path: Path, model: str, doc: str) -> tuple[str | None, str | None]:
    """The tracked document's content and field hashes, or (None, None) if untracked."""
    entry = load_document_shard(documents_shard_path(store_path, model, doc))
    return (entry.hash_c, entry.hash_d) if entry else (None, None)

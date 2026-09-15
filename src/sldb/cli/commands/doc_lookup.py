"""PLAN 15 capa 7: finding a tracked document by name or path, split out of `doc.py` to keep
that file under the clean-code line limit — `_find_doc` was a plain lookup with no state of
its own, so a module-level function serves it exactly as well as a method would."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.core.exceptions import SLDBError
from sldb.store import documents_hash
from sldb.store.io import load_models_index
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path


def find_doc(sp: Path, root: Path, idx: Any, doc_ref: str) -> tuple[Any, Any, Any]:
    """`doc_ref` is usually a name: one cheap shard check per model. Falling back to a match
    by path uses this operation's own cached entries (PLAN 15 capa 8: a doc found by name
    never pays for that; a fallback within an already-composed operation pays nothing new)."""
    for m_entry in idx.models:
        if (doc := load_document_shard(documents_shard_path(sp, m_entry.name, doc_ref))) is not None:
            return m_entry, load_models_index(root / m_entry.models_index), doc
    for m_entry in idx.models:
        if doc := next((d for d in documents_hash.entries_of(sp, m_entry.name) if d.path == doc_ref), None):
            return m_entry, load_models_index(root / m_entry.models_index), doc
    raise SLDBError(f"Doc '{doc_ref}' not found.")

"""Find a tracked document by name or path across a store's models.

Moved here from `sldb.cli.commands.doc_lookup`, which re-exports `find_doc`.
"""

from __future__ import annotations

from pathlib import Path

from sldb.core.exceptions import SLDBError
from sldb.store import documents_hash
from sldb.store.io import load_models_index
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex


def find_doc(sp: Path, root: Path, idx: StoreIndex, doc_ref: str) -> tuple[ModelEntry, ModelsIndex, DocumentEntry]:
    """The model entry, models index and document entry of a tracked document.

    `doc_ref` is usually a name: one cheap shard check per model. Falling back to a match
    by path uses this operation's own cached entries (PLAN 15 capa 8: a doc found by name
    never pays for that; a fallback within an already-composed operation pays nothing new).

    Raises:
        SLDBError: When no model tracks a document with that name or path.
    """
    for m_entry in idx.models:
        if (doc := load_document_shard(documents_shard_path(sp, m_entry.name, doc_ref))) is not None:
            return m_entry, load_models_index(root / m_entry.models_index), doc
    for m_entry in idx.models:
        if doc := next((d for d in documents_hash.entries_of(sp, m_entry.name) if d.path == doc_ref), None):
            return m_entry, load_models_index(root / m_entry.models_index), doc
    raise SLDBError(f"Doc '{doc_ref}' not found.")

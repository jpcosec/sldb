"""Stop tracking a document: drop it from the store indexes, leaving its Markdown file alone."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.document_lookup import find_doc
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.store import documents_hash
from sldb.store.io import load_store_index, save_models_index, store_lock
from sldb.store.io.shards import delete_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.models.store_index import StoreIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


def untrack_document(store: str | Path | None, document: str, pythonpath: str | None = None) -> DocumentReference:
    """Remove a tracked document from its model's index and rebuild the derived indexes.

    Args:
        store: The store tracking the document (path, alias, or None to discover it).
        document: Document name, or its path as recorded in the store.
        pythonpath: Directory to import the store's model modules from.

    Returns:
        The document that was untracked.

    Raises:
        SLDBError: When no model tracks such a document.
    """
    location = open_store(store)
    idx = load_store_index(location.store_path)
    m_entry, m_idx, doc = find_doc(location.store_path, location.project_root, idx, document)
    forget_document(location.store_path, location.project_root, idx, m_entry, m_idx, doc, pythonpath)
    return DocumentReference(model=m_entry.name, name=doc.name, path=location.project_root / doc.path)


def forget_document(sp: Path, root: Path, idx: StoreIndex, m_entry: ModelEntry, m_idx: ModelsIndex, doc: DocumentEntry, pythonpath: str | None) -> None:
    """Delete the document's shard and update model hashes and derived indexes under the store lock."""
    with store_lock(sp):
        delete_shard(documents_shard_path(sp, m_entry.name, doc.name))
        documents_hash.forget(sp, m_entry.name, doc.name)
        m_idx.hash_b = documents_hash.hash_b_of(sp, m_entry.name)
        m_idx.documents_count = documents_hash.count_of(sp, m_entry.name)
        save_models_index(root / m_entry.models_index, m_idx)
        rebuild_semantic_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_sections_indexes(sp, root, resolve_model_ref, pythonpath)
        rebuild_edges_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_hash_a(sp, root, idx)

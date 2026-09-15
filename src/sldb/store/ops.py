from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
from sldb.store.hashing import hash_fields, hash_models_layer, hash_text
from sldb.store.io import (
    load_models_index, save_models_index, save_store_index, store_lock,
)
from sldb.store.io.shards import save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models import DocumentEntry, StoreIndex
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes


class StoreOperations:
    """Operations for the SLDB store."""

    @staticmethod
    def track(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None) -> None:
        StoreOperations._pre_check(store_path, project_root, model_entry, doc_name)
        rel = _get_rel(doc_path, project_root)
        txt = doc_path.read_text(encoding="utf-8")
        with store_lock(store_path):
            StoreOperations._do_track(store_path, project_root, store_index, model_type, model_entry, doc_name, rel, txt, resolve_model_ref, pythonpath)

    @staticmethod
    def _pre_check(store_path, project_root, model_entry, doc_name):
        if documents_shard_path(store_path, model_entry.name, doc_name).exists():
            from sldb.core.exceptions import SLDBStoreError
            raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")

    @staticmethod
    def _do_track(store_path, root, st_idx, m_type, m_entry, d_name, rel_path, text, res_ref, py_path):
        StoreOperations._pre_check(store_path, root, m_entry, d_name)
        entry = DocumentEntry(name=d_name, path=rel_path, hash_c=hash_text(text), hash_d=_safe_hash(m_type, text))
        save_document_shard(documents_shard_path(store_path, m_entry.name, d_name), entry)
        documents_hash.note(store_path, m_entry.name, entry)
        _update_model_summary(store_path, root, m_entry)
        rebuild_semantic_indexes(store_path, root, res_ref, py_path)
        rebuild_sections_indexes(store_path, root, res_ref, py_path)
        cascade_hash_a(store_path, root, st_idx)


def _update_model_summary(store_path: Path, root: Path, m_entry: Any) -> None:
    """hash_b and the document count, from the operation's own child-hash map — no re-read
    of every document shard (PLAN 15 capa 7)."""
    m_idx = load_models_index(root / m_entry.models_index)
    m_idx.hash_b = documents_hash.hash_b_of(store_path, m_entry.name)
    m_idx.documents_count = documents_hash.count_of(store_path, m_entry.name)
    save_models_index(root / m_entry.models_index, m_idx)


def track_document(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None) -> None:
    """Track a document in the store and update hashes."""
    StoreOperations.track(store_path, project_root, store_index, model_type, model_entry, doc_path, doc_name, resolve_model_ref, pythonpath)

def cascade_hash_a(store_path: Path, project_root: Path, store_index: StoreIndex) -> None:
    """Propagate hash updates up to the store level (hash_a)."""
    indices = [load_models_index(project_root / m.models_index) for m in store_index.models]
    store_index.hash_a = hash_models_layer(indices)
    save_store_index(store_path, store_index)

def _get_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)

def _safe_hash(model_type: type, text: str) -> str:
    try:
        return hash_fields(model_type, text)
    except Exception:
        return ""

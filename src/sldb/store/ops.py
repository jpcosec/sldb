from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store.hashing import (
    hash_documents_index,
    hash_fields,
    hash_models_layer,
    hash_text,
)
from sldb.store.io import (
    load_documents_index,
    load_models_index,
    save_documents_index,
    save_models_index,
    save_store_index,
    store_lock,
)
from sldb.store.models import DocumentEntry, StoreIndex
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.core.exceptions import SLDBStoreError


def track_document(
    store_path: Path,
    project_root: Path,
    store_index: StoreIndex,
    model_type: type,
    model_entry: Any,
    doc_path: Path,
    doc_name: str,
    resolve_model_ref: Callable,
    pythonpath: str | None = None,
) -> None:
    """Track a document in the store and update hashes."""
    models_idx = load_models_index(project_root / model_entry.models_index)
    docs_idx = load_documents_index(project_root / models_idx.documents_index)

    if any(d.name == doc_name for d in docs_idx.documents):
        raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")

    rel_path = _get_relative_path(doc_path, project_root)
    text = doc_path.read_text(encoding="utf-8")

    with store_lock(store_path):
        models_idx = load_models_index(project_root / model_entry.models_index)
        docs_idx = load_documents_index(project_root / models_idx.documents_index)

        if any(d.name == doc_name for d in docs_idx.documents):
            raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")

        docs_idx.documents.append(
            DocumentEntry(
                name=doc_name,
                path=rel_path,
                hash_c=hash_text(text),
                hash_d=_safe_hash_fields(model_type, text),
            )
        )

        save_documents_index(project_root / models_idx.documents_index, docs_idx)
        models_idx.hash_b = hash_documents_index(docs_idx)
        save_models_index(project_root / model_entry.models_index, models_idx)

        rebuild_semantic_indexes(
            store_path, project_root, resolve_model_ref, pythonpath
        )
        cascade_hash_a(store_path, project_root, store_index)


def cascade_hash_a(
    store_path: Path, project_root: Path, store_index: StoreIndex
) -> None:
    """Propagate hash updates up to the store level (hash_a)."""
    indices = [
        load_models_index(project_root / m.models_index) for m in store_index.models
    ]
    store_index.hash_a = hash_models_layer(indices)
    save_store_index(store_path, store_index)


def _get_relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _safe_hash_fields(model_type: type, text: str) -> str:
    try:
        return hash_fields(model_type, text)
    except Exception:
        return ""

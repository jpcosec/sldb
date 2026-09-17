"""Register, in a destination store, a model class that a linked store owns.

Moved here from `sldb.cli.federated_utils`, which re-exports these names.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.io import load_store_index, save_documents_index, save_models_index, store_lock
from sldb.store.layout import documents_index_relpath, models_index_relpath
from sldb.store.models.documents_index import DocumentsIndex
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.models_index import ModelsIndex
from sldb.store.ops import cascade_hash_a
from sldb.store.semantic_tags import flatten_model_semantics


def _get_rel_model_path(model_path: Path, root: Path) -> str:
    """Model source path relative to the project root when inside it, else absolute."""
    try:
        return str(model_path.resolve().relative_to(root))
    except ValueError:
        return str(model_path.resolve())


def _save_federated_indexes(root: Path, model_type: type, model_ref: str, rel_model_path: str, mi_rel: str, di_rel: str) -> None:
    """Write an empty documents index and a fresh models index for the federated model."""
    save_documents_index(root / di_rel, DocumentsIndex())
    save_models_index(root / mi_rel, ModelsIndex(name=model_type.__name__, model_ref=model_ref, path=rel_model_path, documents_index=di_rel, hash_b="", version=1, canonical=False, semantics=flatten_model_semantics(model_type)))


def _append_federated_entry(store_path: Path, root: Path, latest_index: Any, model_type: type, model_ref: str, rel_model_path: str, mi_rel: str) -> Any:
    """Add the model entry to the store index and cascade the store hash."""
    entry = ModelEntry(name=model_type.__name__, model_ref=model_ref, path=rel_model_path, models_index=mi_rel, version=1)
    latest_index.models.append(entry)
    cascade_hash_a(store_path, root, latest_index)
    return entry


def _do_ensure_federated_model(store_path: Path, root: Path, model_type: type[StructuredNLDoc], model_ref: str, rel_model_path: str) -> Any:
    """Register the model unless a concurrent writer already did (checked under the lock)."""
    mi_rel, di_rel = models_index_relpath(model_type.__name__), documents_index_relpath(model_type.__name__)
    latest_index = load_store_index(store_path)
    existing = next((e for e in latest_index.models if e.name == model_type.__name__), None)
    if existing is not None:
        return existing
    _save_federated_indexes(root, model_type, model_ref, rel_model_path, mi_rel, di_rel)
    return _append_federated_entry(store_path, root, latest_index, model_type, model_ref, rel_model_path, mi_rel)


def _ensure_federated_model_entry(store_path: Path, root: Path, store_index: Any, model_type: type[StructuredNLDoc], model_ref: str, model_path: Path) -> Any:
    """The destination store's entry for the model, registering it first when missing."""
    existing = next((e for e in store_index.models if e.name == model_type.__name__), None)
    if existing is not None:
        return existing
    rel_model_path = _get_rel_model_path(model_path, root)
    with store_lock(store_path):
        return _do_ensure_federated_model(store_path, root, model_type, model_ref, rel_model_path)

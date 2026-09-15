from __future__ import annotations
from pathlib import Path
from typing import Any
from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.layout import project_root, store_exists, documents_index_relpath, models_index_relpath
from sldb.store.io import load_store_index, save_documents_index, save_models_index, store_lock
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.resolver import ancestor_stores
from sldb.store.models import DocumentsIndex, ModelsIndex, ModelEntry
from sldb.store.semantic_tags import flatten_model_semantics
from sldb.store.ops import cascade_hash_a

def _model_registry_stores(destination_store: Path, local_store: Path | None) -> list[Path]:
    stores = [destination_store]
    if local_store is not None and local_store.resolve() != destination_store.resolve():
        stores.append(local_store.resolve())
    return stores

def _get_linked_store_candidate(registry_store: Path, store_alias: str) -> Path | None:
    registry_root = project_root(registry_store)
    registry_index = load_store_index(registry_store)
    linked = next((e for e in registry_index.stores if e.name == store_alias), None)
    if linked is None:
        return None
    linked_path = Path(linked.path)
    candidate = (linked_path if linked_path.is_absolute() else registry_root / linked_path).resolve()
    return candidate if store_exists(candidate) else None

def _resolve_linked_store(destination_store: Path, store_alias: str) -> Path | None:
    registries = _model_registry_stores(destination_store, next(iter(ancestor_stores()), None))
    for registry_store in registries:
        candidate = _get_linked_store_candidate(registry_store, store_alias)
        if candidate is not None:
            return candidate
    return None

def _load_remote_entry(linked_store: Path, remote_model_name: str) -> Any:
    linked_index = load_store_index(linked_store)
    return next((e for e in linked_index.models if e.name == remote_model_name), None)

def _build_federated_entry(destination_store: Path, linked_store: Path, remote_entry: Any, pythonpath: str | None) -> tuple[type, Any, Any]:
    model_type = resolve_model_ref(remote_entry.model_ref, pythonpath)
    local_entry = _ensure_federated_model_entry(destination_store, project_root(destination_store), load_store_index(destination_store), model_type, remote_entry.model_ref, project_root(linked_store) / remote_entry.path)
    return model_type, local_entry, load_store_index(destination_store)

def _find_federated_model(destination_store: Path, model_name: str, pythonpath: str | None) -> tuple[type, Any, Any] | None:
    if ":" not in model_name:
        return None
    store_alias, remote_model_name = model_name.split(":", 1)
    linked_store = _resolve_linked_store(destination_store, store_alias)
    if linked_store is None:
        return None
    remote_entry = _load_remote_entry(linked_store, remote_model_name)
    if remote_entry is None:
        return None
    return _build_federated_entry(destination_store, linked_store, remote_entry, pythonpath)

def _get_rel_model_path(model_path: Path, root: Path) -> str:
    try:
        return str(model_path.resolve().relative_to(root))
    except ValueError:
        return str(model_path.resolve())

def _save_federated_indexes(root: Path, model_type: type, model_ref: str, rel_model_path: str, mi_rel: str, di_rel: str) -> None:
    save_documents_index(root / di_rel, DocumentsIndex())
    save_models_index(root / mi_rel, ModelsIndex(name=model_type.__name__, model_ref=model_ref, path=rel_model_path, documents_index=di_rel, hash_b="", version=1, canonical=False, semantics=flatten_model_semantics(model_type)))

def _append_federated_entry(store_path: Path, root: Path, latest_index: Any, model_type: type, model_ref: str, rel_model_path: str, mi_rel: str) -> Any:
    entry = ModelEntry(name=model_type.__name__, model_ref=model_ref, path=rel_model_path, models_index=mi_rel, version=1)
    latest_index.models.append(entry)
    cascade_hash_a(store_path, root, latest_index)
    return entry

def _do_ensure_federated_model(store_path: Path, root: Path, model_type: type[StructuredNLDoc], model_ref: str, rel_model_path: str) -> Any:
    mi_rel, di_rel = models_index_relpath(model_type.__name__), documents_index_relpath(model_type.__name__)
    latest_index = load_store_index(store_path)
    existing = next((e for e in latest_index.models if e.name == model_type.__name__), None)
    if existing is not None:
        return existing
    _save_federated_indexes(root, model_type, model_ref, rel_model_path, mi_rel, di_rel)
    return _append_federated_entry(store_path, root, latest_index, model_type, model_ref, rel_model_path, mi_rel)

def _ensure_federated_model_entry(store_path: Path, root: Path, store_index: Any, model_type: type[StructuredNLDoc], model_ref: str, model_path: Path) -> Any:
    existing = next((e for e in store_index.models if e.name == model_type.__name__), None)
    if existing is not None:
        return existing
    rel_model_path = _get_rel_model_path(model_path, root)
    with store_lock(store_path):
        return _do_ensure_federated_model(store_path, root, model_type, model_ref, rel_model_path)

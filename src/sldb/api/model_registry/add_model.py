"""Register a model class in a store so documents of that model can be tracked."""

from __future__ import annotations

import inspect
from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_registry.model_index_writes import relative_model_path, write_new_model_indexes
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store.io import load_store_index
from sldb.store.layout import documents_index_relpath, models_index_relpath
from sldb.store.models.store_index import StoreIndex


def add_model(store: str | Path | None, model_ref: str, pythonpath: str | None = None, canonical: bool = False, actor: str | None = None) -> ModelRegistration:
    """Register the model class a reference names, with an empty documents index.

    Args:
        store: The store to register in (path, alias, or None to discover it).
        model_ref: `module:ClassName` reference of a StructuredNLDoc subclass.
        pythonpath: Directory to import the model module from.
        canonical: Mark the model as the canonical one of its family.
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The new registry record (version 1).

    Raises:
        SLDBModelError: When the reference cannot be imported or the model is already registered.
    """
    location = open_store(store)
    model_type = resolve_model_ref(model_ref, pythonpath)
    idx = load_store_index(location.store_path)
    name = model_type.__name__
    _refuse_duplicate(idx, name)
    before = store_hash(location.store_path)
    mi = _write_indexes(location.store_path, location.project_root, idx, model_type, model_ref, canonical, pythonpath)
    record(location.store_path, {"operation": "add_model", "address": mi.name, "new_value": mi.model_ref, "hash_a_before": before, "hash_a_after": store_hash(location.store_path), "actor": actor})
    return ModelRegistration(name=mi.name, model_ref=mi.model_ref, path=mi.path, version=mi.version)


def _write_indexes(sp: Path, root: Path, idx: StoreIndex, model_type: type, model_ref: str, canonical: bool, pythonpath: str | None):
    m_path = relative_model_path(Path(inspect.getfile(model_type)), root)
    return write_new_model_indexes(sp, root, idx, model_type, model_ref, m_path, models_index_relpath(model_type.__name__), documents_index_relpath(model_type.__name__), canonical, pythonpath)


def _refuse_duplicate(idx: StoreIndex, name: str) -> None:
    if any(m.name == name for m in idx.models):
        raise SLDBModelError(f"Model '{name}' exists.")

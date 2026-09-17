"""Register a model class in a store so documents of that model can be tracked."""

from __future__ import annotations

import inspect
from pathlib import Path

from sldb.api.model_registry.model_index_writes import relative_model_path, write_new_model_indexes
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store.io import load_store_index
from sldb.store.layout import documents_index_relpath, models_index_relpath


def add_model(store: str | Path | None, model_ref: str, pythonpath: str | None = None, canonical: bool = False) -> ModelRegistration:
    """Register the model class a reference names, with an empty documents index.

    Args:
        store: The store to register in (path, alias, or None to discover it).
        model_ref: `module:ClassName` reference of a StructuredNLDoc subclass.
        pythonpath: Directory to import the model module from.
        canonical: Mark the model as the canonical one of its family.

    Returns:
        The new registry record (version 1).

    Raises:
        SLDBModelError: When the reference cannot be imported or the model is already registered.
    """
    location = open_store(store)
    model_type = resolve_model_ref(model_ref, pythonpath)
    idx = load_store_index(location.store_path)
    name = model_type.__name__
    if any(m.name == name for m in idx.models):
        raise SLDBModelError(f"Model '{name}' exists.")
    m_path = relative_model_path(Path(inspect.getfile(model_type)), location.project_root)
    mi = write_new_model_indexes(location.store_path, location.project_root, idx, model_type, model_ref, m_path, models_index_relpath(name), documents_index_relpath(name), canonical, pythonpath)
    return ModelRegistration(name=mi.name, model_ref=mi.model_ref, path=mi.path, version=mi.version)

"""Look up a model registered in a store (or in a linked store) and import its class."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.federated_lookup import _find_federated_model
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index


def load_registered_model(store_path: Path, model_name: str, pythonpath: str | None = None) -> RegisteredModel:
    """Resolve a registered model name to its class and registry entry.

    Args:
        store_path: An already resolved `.sldb` directory (see `open_store`).
        model_name: A model name registered in the store, or `alias:ModelName` for a model
            owned by a linked store (registered locally on first use).
        pythonpath: Directory to import the model module from.

    Returns:
        The model class, its entry, and the store index holding the entry.

    Raises:
        SLDBStoreError: When no such model is registered.
        SLDBModelError: When the registered reference cannot be imported.
    """
    idx = load_store_index(store_path)
    entry = next((m for m in idx.models if m.name == model_name), None)
    if entry is not None:
        return RegisteredModel(model_type=resolve_model_ref(entry.model_ref, pythonpath), entry=entry, store_index=idx)
    federated = _find_federated_model(store_path, model_name, pythonpath)
    if federated is None:
        raise SLDBStoreError(f"Model '{model_name}' not registered.")
    model_type, federated_entry, federated_index = federated
    return RegisteredModel(model_type=model_type, entry=federated_entry, store_index=federated_index)

"""Unregister a model that tracks no documents (the inverse of `add_model`)."""

from __future__ import annotations

from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_registry.model_files import drop_model_files
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store import documents_hash
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.io import load_models_index, load_store_index, save_store_index, store_lock
from sldb.store.ops import cascade_store_hash


def remove_model(store: str | Path | None, model_name: str, pythonpath: str | None = None, actor: str | None = None) -> ModelRegistration:
    """Unregister a model: its entry, indexes and shards go; its class is never imported.

    Args:
        store: The store (path, alias, or None to discover it).
        model_name: The registered model's name.
        pythonpath: Directory to import the remaining models from (derived indexes are rebuilt).
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The registry record that was removed.

    Raises:
        SLDBModelError: The model is not registered, or still tracks documents (untrack them first).
    """
    location = open_store(store)
    sp, root = location.store_path, location.project_root
    idx = load_store_index(sp)
    entry = _removable(sp, idx, model_name)
    before = store_hash(sp)
    _unregister(sp, root, idx, entry, pythonpath)
    record(sp, {"operation": "remove_model", "address": entry.name, "previous_value": entry.model_ref, "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})
    return ModelRegistration(name=entry.name, model_ref=entry.model_ref, path=entry.path, version=entry.version)


def _unregister(sp: Path, root: Path, idx, entry, pythonpath: str | None) -> None:
    with store_lock(sp):
        documents_index = load_models_index(root / entry.models_index).documents_index
        idx.models.remove(entry)
        save_store_index(sp, idx)  # the rebuilds below read the registry from disk
        drop_model_files(sp, root, entry.name, entry.models_index, documents_index)
        rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, idx)


def _removable(sp: Path, idx, model_name: str):
    entry = next((m for m in idx.models if m.name == model_name), None)
    if entry is None:
        raise SLDBModelError(f"Model '{model_name}' is not registered.")
    count = documents_hash.count_of(sp, model_name)
    if count:
        raise SLDBModelError(f"Model '{model_name}' still tracks {count} document(s); untrack them first (`sldb docs untrack`).")
    return entry

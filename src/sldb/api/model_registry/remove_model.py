"""Unregister a model (the inverse of `add_model`), with its documents only when asked."""

from __future__ import annotations

from pathlib import Path

from sldb.api.model_registry.model_files import drop_model_files, forget_store_caches
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError
from sldb.store import documents_hash
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.io import load_models_index, load_store_index, save_store_index, store_lock
from sldb.store.io.rollback import rollback_on_error
from sldb.store.layout import store_index_path
from sldb.store.ops import cascade_store_hash


def remove_model(store: str | Path | None, model_name: str, pythonpath: str | None = None, actor: str | None = None, untrack_documents: bool = False) -> ModelRegistration:
    """Unregister a model: its entry, indexes and shards go; its class is never imported.

    Args:
        store: The store (path, alias, or None to discover it).
        model_name: The registered model's name.
        pythonpath: Directory to import the remaining models from (derived indexes are rebuilt).
        actor: Optional caller label; accepted for compatibility, no longer recorded (the journal was retired on 2026-11-04).
        untrack_documents: Also stop tracking its documents (their Markdown files stay), the
            way to drop a model whose class was deleted while documents were tracked.

    Returns:
        The registry record that was removed.

    Raises:
        SLDBModelError: The model is not registered, or still tracks documents and
            `untrack_documents` is False.
    """
    location = open_store(store)
    sp, root = location.store_path, location.project_root
    idx = load_store_index(sp)
    entry = _removable(sp, idx, model_name, untrack_documents)
    _unregister(sp, root, idx, entry, pythonpath)
    return ModelRegistration(name=entry.name, model_ref=entry.model_ref, path=entry.path, version=entry.version)


def _unregister(sp: Path, root: Path, idx, entry, pythonpath: str | None) -> None:
    """Registry first, files last: if a rebuild raises, the store index is put back and the
    model's files were never touched."""
    with store_lock(sp):
        documents_index = load_models_index(root / entry.models_index).documents_index
        with rollback_on_error([store_index_path(sp)], lambda: forget_store_caches(sp, entry.name)):
            idx.models.remove(entry)
            save_store_index(sp, idx)  # the rebuilds below read the registry from disk
            rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
            cascade_store_hash(sp, root, idx)
        drop_model_files(sp, root, entry.name, entry.models_index, documents_index)


def _removable(sp: Path, idx, model_name: str, untrack_documents: bool):
    entry = next((m for m in idx.models if m.name == model_name), None)
    if entry is None:
        raise SLDBModelError(f"Model '{model_name}' is not registered.")
    count = documents_hash.count_of(sp, model_name)
    if count and not untrack_documents:
        raise SLDBModelError(f"Model '{model_name}' still tracks {count} document(s); untrack them first, or remove them with it (`sldb models remove --with-documents`).")
    return entry

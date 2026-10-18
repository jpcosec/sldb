"""Inherit a model from the linked store that owns it, instead of keeping a copy of it."""

from __future__ import annotations

from pathlib import Path

from sldb.api.journal import record, store_hash
from sldb.api.model_registry.federated_registration import _do_ensure_federated_model
from sldb.api.model_registry.model_reference import add_import_roots, resolve_model_ref, same_model_class
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBModelError, SLDBStoreError
from sldb.store.derived_rebuild import rebuild_derived_indexes
from sldb.store.io import load_models_index, load_store_index, save_models_index, save_store_index, store_lock
from sldb.store.layout import project_root
from sldb.store.model_origin import linked_store
from sldb.store.ops import cascade_store_hash


def inherit_model(store: str | Path | None, ref: str, pythonpath: str | None = None, actor: str | None = None) -> ModelRegistration:
    """Register `alias:ModelName` as inherited from the store linked as `alias`.

    A copy of that model already registered here (same `model_ref`) is converted in place:
    its documents, roster and signed contract stay; only the source path goes, and the class
    imports from the owner's project root from then on. If the owner's class has moved since
    this store signed it, `stores check` reports `contract moved` and `stores update` fixes it.

    Args:
        store: The store (path, alias, or None to discover it).
        ref: `alias:ModelName`, the alias being a store this store links (`stores add`).
        pythonpath: Directory to import the store's other models from (indexes are rebuilt).
        actor: Optional label recorded in the store journal for this write.

    Returns:
        The inherited entry's registry record.

    Raises:
        SLDBStoreError: The alias is not linked, or the linked store does not own the model.
        SLDBModelError: A model of that name here is another class (an override: give it a name
            of its own that extends the owner's), or it already inherits from another store.
    """
    alias, name = _split(ref)
    location = open_store(store)
    sp, root = location.store_path, location.project_root
    theirs = _owners_entry(sp, alias, name)
    before = store_hash(sp)
    entry = _commit(sp, root, alias, theirs, pythonpath)
    record(sp, {"operation": "inherit_model", "address": name, "previous_value": None, "new_value": {"origin": alias}, "hash_a_before": before, "hash_a_after": store_hash(sp), "actor": actor})
    return ModelRegistration(name=entry.name, model_ref=entry.model_ref, path=entry.path, version=entry.version)


def _commit(sp: Path, root: Path, alias: str, theirs, pythonpath: str | None):
    """Under the store lock: the entry, then the derived indexes and the root hash."""
    with store_lock(sp):
        entry = _inherit(sp, root, alias, theirs)
        rebuild_derived_indexes(sp, root, resolve_model_ref, pythonpath)
        cascade_store_hash(sp, root, load_store_index(sp))
    return entry


def _owners_entry(sp: Path, alias: str, name: str):
    """The owner's entry for the model, with the owner's root put on the import path."""
    owner = linked_store(sp, alias)
    if owner is None:
        raise SLDBStoreError(f"No store is linked as '{alias}' (see `sldb stores add`).")
    theirs = next((m for m in load_store_index(owner).models if m.name == name and not m.origin), None)
    if theirs is None:
        raise SLDBStoreError(f"The store linked as '{alias}' does not own a model named '{name}'.")
    add_import_roots([project_root(owner)])
    return theirs


def _split(ref: str) -> tuple[str, str]:
    alias, sep, name = ref.partition(":")
    if not sep or not alias or not name:
        raise SLDBModelError(f"'{ref}' is not 'alias:ModelName'.")
    return alias, name


def _inherit(sp: Path, root: Path, alias: str, theirs):
    """Convert the local copy, or register a new inherited entry; a no-op when already inherited."""
    idx = load_store_index(sp)
    mine = next((m for m in idx.models if m.name == theirs.name), None)
    if mine is None:
        return _do_ensure_federated_model(sp, root, resolve_model_ref(theirs.model_ref), theirs.model_ref, "", alias)
    if mine.origin == alias:
        return mine
    _refuse_non_copy(mine, theirs)
    return _convert_copy(sp, root, idx, mine, alias, theirs)


def _refuse_non_copy(mine, theirs) -> None:
    if mine.origin:
        raise SLDBModelError(f"'{mine.name}' already inherits from the store linked as '{mine.origin}'.")
    if not same_model_class(mine.model_ref, theirs.model_ref):
        raise SLDBModelError(f"'{mine.name}' here is another class ({mine.model_ref}, theirs {theirs.model_ref}): an override. Give it a name of its own that extends theirs, or remove it first.")


def _convert_copy(sp: Path, root: Path, idx, mine, alias: str, theirs):
    """The copy keeps its documents, roster and signed contract; its source path goes, and it
    names the class with the owner's reference."""
    mine.origin, mine.path, mine.model_ref = alias, "", theirs.model_ref
    m_idx = load_models_index(root / mine.models_index)
    m_idx.path, m_idx.model_ref = "", theirs.model_ref
    save_models_index(root / mine.models_index, m_idx)
    save_store_index(sp, idx)
    return mine

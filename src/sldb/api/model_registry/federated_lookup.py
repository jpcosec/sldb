"""Find a model that a linked store registers, addressed as `alias:ModelName`.

Moved here from `sldb.cli.federated_utils`, which re-exports these names.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_registry.federated_registration import _ensure_federated_model_entry
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists
from sldb.store.resolver import ancestor_stores


def _model_registry_stores(destination_store: Path, local_store: Path | None) -> list[Path]:
    """Stores whose links may name the alias: the destination, then the local project store."""
    stores = [destination_store]
    if local_store is not None and local_store.resolve() != destination_store.resolve():
        stores.append(local_store.resolve())
    return stores


def _get_linked_store_candidate(registry_store: Path, store_alias: str) -> Path | None:
    """The existing store a registry links under `store_alias`, if any."""
    registry_root = project_root(registry_store)
    registry_index = load_store_index(registry_store)
    linked = next((e for e in registry_index.stores if e.name == store_alias), None)
    if linked is None:
        return None
    linked_path = Path(linked.path)
    candidate = (linked_path if linked_path.is_absolute() else registry_root / linked_path).resolve()
    return candidate if store_exists(candidate) else None


def _resolve_linked_store(destination_store: Path, store_alias: str) -> Path | None:
    """The first registry link that resolves `store_alias` to an existing store."""
    registries = _model_registry_stores(destination_store, next(iter(ancestor_stores()), None))
    for registry_store in registries:
        candidate = _get_linked_store_candidate(registry_store, store_alias)
        if candidate is not None:
            return candidate
    return None


def _load_remote_entry(linked_store: Path, remote_model_name: str) -> Any:
    """The linked store's registry entry for a model name, if registered there."""
    linked_index = load_store_index(linked_store)
    return next((e for e in linked_index.models if e.name == remote_model_name), None)


def _build_federated_entry(destination_store: Path, linked_store: Path, remote_entry: Any, pythonpath: str | None) -> tuple[type, Any, Any]:
    """Import the remote model and make sure the destination store registers it too."""
    model_type = resolve_model_ref(remote_entry.model_ref, pythonpath)
    local_entry = _ensure_federated_model_entry(destination_store, project_root(destination_store), load_store_index(destination_store), model_type, remote_entry.model_ref, project_root(linked_store) / remote_entry.path)
    return model_type, local_entry, load_store_index(destination_store)


def _find_federated_model(destination_store: Path, model_name: str, pythonpath: str | None) -> tuple[type, Any, Any] | None:
    """Resolve `alias:ModelName` through a linked store; None when it names no such model."""
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

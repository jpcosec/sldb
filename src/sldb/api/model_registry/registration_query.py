"""Which models a store has registered, asked without reading its index files.

deskops checks at init and in its health commands that every model it expects is registered
(inbox 20260614-000003); it had to parse `store_index.yaml` itself.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.io import load_store_index
from sldb.store.models.model_entry import ModelEntry


def registered_models(store: str | Path | None) -> list[ModelEntry]:
    """Every model the store registers (its own and the ones it inherits), sorted by name.

    Args:
        store: The store (path, alias, or None to discover it).
    """
    return sorted(load_store_index(open_store(store).store_path).models, key=lambda m: m.name)


def is_model_registered(store: str | Path | None, model: str) -> bool:
    """Whether `model` is registered: by name (`TaskDoc`), or by reference
    (`deskops.models:TaskDoc` or `deskops.models.TaskDoc`)."""
    return any(model in _names(entry) for entry in registered_models(store))


def _names(entry: ModelEntry) -> set[str]:
    return {entry.name, entry.model_ref, entry.model_ref.replace(":", ".")}

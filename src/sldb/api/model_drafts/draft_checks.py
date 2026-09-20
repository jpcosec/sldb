"""The registry facts a draft validation needs; document checks live in `backfill`."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store.io import load_models_index, load_store_index


def current_version(store: str | Path | None, model_name: str) -> int:
    """The contract version the store's models index records for a model (1 when unregistered)."""
    location = open_store(store)
    entry = next((m for m in load_store_index(location.store_path).models if m.name == model_name), None)
    return load_models_index(location.project_root / entry.models_index).version if entry else 1

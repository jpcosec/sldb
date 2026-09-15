"""Maintain explicit global knowledge of project stores."""
from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_store_index, save_store_index
from sldb.store.models import StoreEntry
from sldb.store.resolver import global_store_path


def register_project_store(store_path: Path) -> None:
    """Register a store under HOME in the global catalog, once per path."""
    global_store = global_store_path().resolve()
    candidate = store_path.resolve()
    if candidate == global_store or not candidate.is_relative_to(Path.home().resolve()):
        return
    index = load_store_index(global_store)
    if any(_entry_path(global_store, entry.path) == candidate for entry in index.stores):
        return
    index.stores.append(StoreEntry(name=candidate.parent.name, path=str(candidate)))
    save_store_index(global_store, index)


def _entry_path(store_path: Path, value: str) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else store_path.parent / path).resolve()

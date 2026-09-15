"""Explicit discovery and reconciliation for a store catalog."""
from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_store_index, save_store_index
from sldb.store.layout import project_root, store_exists
from sldb.store.models import StoreEntry


def reconcile_catalog(catalog: Path, search_root: Path, apply: bool) -> dict:
    """Compare an explicit subtree with a catalog; mutate only with apply."""
    index = load_store_index(catalog)
    found = _found_stores(search_root, catalog)
    registered = _registered_stores(catalog, index.stores)
    report = _report(found, registered)
    if apply:
        index.stores = _entries(found)
        save_store_index(catalog, index)
    return report


def _found_stores(root: Path, catalog: Path) -> list[Path]:
    return sorted({path.resolve() for path in root.rglob(".sldb") if path.resolve() != catalog.resolve() and store_exists(path)})


def _registered_stores(catalog: Path, entries: list[StoreEntry]) -> set[Path]:
    return {(Path(entry.path) if Path(entry.path).is_absolute() else project_root(catalog) / entry.path).resolve() for entry in entries}


def _report(found: list[Path], registered: set[Path]) -> dict:
    current = set(found)
    return {"discovered": [str(path) for path in found], "missing": [str(path) for path in sorted(current - registered)],
            "stale": [str(path) for path in sorted(path for path in registered if not store_exists(path))]}


def _entries(found: list[Path]) -> list[StoreEntry]:
    return [StoreEntry(name=path.parent.name, path=str(path)) for path in found]

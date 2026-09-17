"""Create a new, empty store in a project directory."""

from __future__ import annotations

import shutil
from pathlib import Path

from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_skeleton import register_in_global_catalog, write_empty_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.layout import store_exists


def init_store(path: str | Path = ".", force: bool = False) -> StoreLocation:
    """Create `<path>/.sldb` and register it in the global store's catalog when it is under HOME.

    Args:
        path: The project root that will hold the `.sldb` directory.
        force: Delete an existing store there and create it again, empty.

    Returns:
        The new store's `.sldb` directory and project root.

    Raises:
        SLDBStoreError: When a store already exists at `path` and `force` is False.
    """
    root = Path(path).resolve()
    store_path = root / ".sldb"
    if store_exists(store_path):
        _replace_existing(store_path, force)
    write_empty_store(store_path)
    register_in_global_catalog(store_path)
    return StoreLocation(store_path=store_path, project_root=root)


def _replace_existing(store_path: Path, force: bool) -> None:
    """Delete an existing store when forced; refuse otherwise."""
    if not force:
        raise SLDBStoreError(f"Store already exists at {store_path}. Use --force to reinitialize.")
    shutil.rmtree(store_path)

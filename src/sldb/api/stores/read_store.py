"""Read a store without migrating it: a fresh read-only operation over a prepared store."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_discovery import _find_default_store, _resolve_store_arg
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBStoreError
from sldb.store.documents_hash import new_operation as new_documents_hash_operation
from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists, store_index_path
from sldb.store.migration import _already_canonical
from sldb.store.model_origin import add_owner_import_roots
from sldb.store.runtime_cache_signature import new_operation

NOT_PREPARED = "store not prepared: run `sldb stores update`"


def store_is_prepared(store: Path) -> bool:
    """True when the store exists and its layout is already canonical (nothing to migrate).

    Args:
        store: The store's `.sldb` directory.
    """
    store_path = Path(store)
    if not store_exists(store_path) or not store_index_path(store_path).exists():
        return False
    return _already_canonical(load_store_index(store_path), store_path, project_root(store_path))


def read_store(store: str | Path | None = None) -> StoreLocation:
    """Resolve a store and start a new read-only operation over it, never writing to disk.

    Unlike `open_store`, the layout is never migrated: a reader (a GET) must not rewrite the
    store it reads. Each call starts a new operation, so documents added or removed by another
    process since the previous call are seen.

    Args:
        store: A `.sldb` directory path, the alias of a linked store, or None/"" to discover
            the nearest project store (falling back to the global store, as `mode="readonly"`).

    Returns:
        The resolved store directory and its project root.

    Raises:
        SLDBStoreError: When no store can be found, or when its layout is not canonical
            ("store not prepared: run `sldb stores update`").
    """
    store_path = _resolve_store_arg(str(store)) if store else _find_default_store("readonly")
    root = project_root(store_path)
    if not store_is_prepared(store_path):
        raise SLDBStoreError(f"{NOT_PREPARED} ({store_path})")
    add_owner_import_roots(store_path)  # inherited models import from their owner
    new_operation(store_path)
    new_documents_hash_operation(store_path)
    return StoreLocation(store_path=store_path, project_root=root)

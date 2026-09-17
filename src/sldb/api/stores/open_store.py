"""Open a store: resolve where it lives and start a fresh sldb operation over it."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_discovery import _find_default_store, _resolve_store_arg
from sldb.api.stores.store_location import StoreLocation
from sldb.store.documents_hash import new_operation as new_documents_hash_operation
from sldb.store.layout import project_root, store_exists
from sldb.store.migration import migrate_store_layout
from sldb.store.runtime_cache_signature import new_operation


def open_store(store: str | Path | None = None, mode: str = "default") -> StoreLocation:
    """Resolve a store argument and start a new operation over that store.

    Every library operation opens its store this way, exactly as each sldb CLI command
    does: the layout is migrated if needed and the per-operation document re-check
    (PLAN 15 capa 6) is scheduled.

    Args:
        store: A `.sldb` directory path, the alias of a linked store, or None/"" to
            discover the nearest project store from the working directory.
        mode: "readonly" lets discovery fall back to the global store with a warning;
            any other value refuses that fallback.

    Returns:
        The resolved store directory and its project root.

    Raises:
        SLDBStoreError: When no store is given and none can be discovered.
    """
    store_path = _resolve_store_arg(str(store)) if store else _find_default_store(mode)
    root = project_root(store_path)
    if store_exists(store_path):
        migrate_store_layout(store_path, root)
    new_operation(store_path)
    new_documents_hash_operation(store_path)
    return StoreLocation(store_path=store_path, project_root=root)

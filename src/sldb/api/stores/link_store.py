"""Link one store into another so its documents can be read through the linking store."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index
from sldb.store.layout import store_exists
from sldb.store.models.store_entry import StoreEntry
from sldb.store.models.store_index import StoreIndex


def link_store(store: str | Path | None, other_store: str | Path, name: str | None = None) -> LinkedStore:
    """Record another store as linked into `store`.

    Args:
        store: The linking store (path, alias, or None to discover it).
        other_store: Path of the `.sldb` directory to link.
        name: Alias for the link; defaults to the name of the directory holding `other_store`.

    Returns:
        The link as recorded in the store index.

    Raises:
        SLDBStoreError: When `other_store` is not a store or the name is already linked.
    """
    location = open_store(store)
    other = Path(other_store).resolve()
    _check_other_exists(other)
    link_name = name or other.parent.name
    path = record_store_link(location.store_path, location.project_root, other, link_name)
    return LinkedStore(name=link_name, path=path)


def _check_other_exists(other: Path) -> None:
    """Refuse to link a directory that holds no store."""
    if not store_exists(other):
        raise SLDBStoreError(f"No store at {other}")


def _check_store_linked(idx: StoreIndex, name: str) -> None:
    """Refuse a link name the store index already uses."""
    if any(s.name == name for s in idx.stores):
        raise SLDBStoreError(f"Store '{name}' already linked.")


def record_store_link(sp: Path, root: Path, other: Path, name: str) -> str:
    """Append a link entry to the store index without checking that `other` exists.

    Args:
        sp: The linking store's `.sldb` directory.
        root: The linking store's project root.
        other: Resolved `.sldb` directory being linked.
        name: Alias for the link.

    Returns:
        The path recorded for the link.

    Raises:
        SLDBStoreError: When the name is already linked.
    """
    idx = load_store_index(sp)
    _check_store_linked(idx, name)
    rel = str(other.relative_to(root)) if other.is_relative_to(root) else str(other)
    idx.stores.append(StoreEntry(name=name, path=rel))
    save_store_index(sp, idx)
    return rel

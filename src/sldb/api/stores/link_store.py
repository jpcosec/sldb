"""Link one store into another so its documents can be read through the linking store."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.api.stores.doc_ref import LINK_NAME, LOCAL
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
        SLDBStoreError: When `other_store` is not a store or is the linking store itself, or
            the name is invalid, reserved (`local`) or already linked.
    """
    location = open_store(store)
    other = Path(other_store).resolve()
    _check_other_exists(other)
    _check_not_self(location.store_path, other)
    link_name = name or other.parent.name
    _check_link_name(link_name)
    path = record_store_link(location.store_path, location.project_root, other, link_name)
    return LinkedStore(name=link_name, path=path)


def _check_other_exists(other: Path) -> None:
    """Refuse to link a directory that holds no store."""
    if not store_exists(other):
        raise SLDBStoreError(f"No store at {other}")


def _check_not_self(store_path: Path, other: Path) -> None:
    """Refuse to link a store into itself."""
    if store_path.resolve() == other:
        raise SLDBStoreError(f"A store cannot link to itself: {other}")


def _check_link_name(name: str) -> None:
    """Refuse an alias `alias:doc` references could not name, and the reserved `local`."""
    if not LINK_NAME.match(name) or name == LOCAL:
        raise SLDBStoreError(f"Invalid link name '{name}': use letters, digits, '.', '_' or '-' (starting with a letter or digit), not 'local'. Pass --name.")


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
        The path recorded for the link, always relative to `root` so the link survives a
        checkout of both repos at another location.

    Raises:
        SLDBStoreError: When the name is already linked.
    """
    idx = load_store_index(sp)
    _check_store_linked(idx, name)
    rel = os.path.relpath(other, root)
    idx.stores.append(StoreEntry(name=name, path=rel))
    save_store_index(sp, idx)
    return rel

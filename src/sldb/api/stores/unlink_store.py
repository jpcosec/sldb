"""Remove a store link, or let `link_store(..., replace=True)` point it somewhere else.

A link left pointing at a directory that is gone (a worktree a run linked from, then deleted)
could only be fixed by editing `store_index.yaml` by hand: `link_store` refuses a name already
linked, and nothing removed one.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index, save_store_index


def unlink_store(store: str | Path | None, name: str) -> LinkedStore:
    """Forget the store linked as `name`; its own store is not touched.

    Args:
        store: The linking store (path, alias, or None to discover it).
        name: The link's alias.

    Returns:
        The link as it was recorded.

    Raises:
        SLDBStoreError: When nothing is linked as `name`, or a model here is inherited from it
            (it imports from there: point the link elsewhere with `link_store(..., replace=True)`).
    """
    sp = open_store(store).store_path
    heirs = [m.name for m in load_store_index(sp).models if m.origin == name]
    if heirs:
        raise SLDBStoreError(f"Store '{name}' is where {', '.join(heirs)} import from: link it again elsewhere (`sldb stores add <path> --name {name} --replace`) instead of removing it.")
    return drop_link(sp, name)


def drop_link(sp: Path, name: str) -> LinkedStore:
    """Remove the entry `name` from the store index; refused when there is none."""
    idx = load_store_index(sp)
    entry = next((s for s in idx.stores if s.name == name), None)
    if entry is None:
        raise SLDBStoreError(f"No store linked as '{name}'.")
    idx.stores = [s for s in idx.stores if s.name != name]
    save_store_index(sp, idx)
    return LinkedStore(name=entry.name, path=entry.path)

"""Writes to the semantic DAG, reflected in the edge index at once.

Every other write that goes through `sldb.api` leaves the edge index current; these follow
the same rule. A new `semantic_parent` edge is visible to `sldb graph` and to `se.` the
moment the call returns.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.open_store import open_store
from sldb.store import semantic as store_semantic
from sldb.store import semantic_parents
from sldb.store.edge_rebuild import refresh_store_edges
from sldb.store.io import load_semantic_dag


def add_semantic_parent(store: str | Path | None, tag: str, parent: str, actor: str | None = None) -> bool:
    """Declare `tag` a kind of `parent`. True when the DAG changed, False when it already said so.

    Raises:
        SLDBStoreError: When either tag is unknown, or the edge would close a cycle.
    """
    sp = open_store(store).store_path
    return _refreshing(sp, lambda: semantic_parents.add_semantic_parent(sp, tag, parent))


def remove_semantic_parent(store: str | Path | None, tag: str, parent: str, actor: str | None = None) -> bool:
    """Undeclare it. True when the DAG changed.

    Raises:
        SLDBStoreError: When the parent is the one the tag's own name implies.
    """
    sp = open_store(store).store_path
    return _refreshing(sp, lambda: semantic_parents.remove_semantic_parent(sp, tag, parent))


def add_semantic_equivalence(store: str | Path | None, local_tag: str, global_tag: str, actor: str | None = None) -> bool:
    """Map a local tag to a global one, for `gse.` across linked stores. True when the DAG
    changed. The store function this wraps existed for a long time with no caller at all."""
    sp = open_store(store).store_path
    return _refreshing(sp, lambda: _add_equivalence(sp, local_tag, global_tag))


def _add_equivalence(sp: Path, local_tag: str, global_tag: str) -> bool:
    if global_tag in load_semantic_dag(sp).equivalences.get(local_tag, []):
        return False
    store_semantic.add_semantic_equivalence(sp, local_tag, global_tag)
    return True


def _refreshing(sp: Path, write) -> bool:
    """`actor` on the public functions is accepted for compatibility; the journal that recorded it was retired on 2026-11-04."""
    changed = bool(write())
    if changed:
        refresh_store_edges(sp)
    return changed

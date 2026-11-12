"""How `compose_edge_index` gets its index in a process that has none (H11): the one an earlier
process kept on disk (`composed_disk`), else composed from the shards and kept; and the
documents a file edited from outside left stale, checked on every read."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from sldb.store.edge_index.composed_disk import disk_key, load_composed, save_composed
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.live_stale import ModelTypeOf, live_facts, stale_of_facts

Stores = list[tuple[Path, str | None]]


def read_or_compose(stores: Stores, include_linked: bool, exclude_tags: frozenset[str], model_type_of: ModelTypeOf | None, compose: Callable) -> tuple[EdgeIndex, list]:
    """(index, each store's `live_facts`): as an earlier process composed it from these very
    shards, else composed now by `compose(stores, exclude_tags, model_type_of)` and kept."""
    key = disk_key(stores, include_linked, exclude_tags, model_type_of)
    found = load_composed(stores[0][0], key)
    if found is not None:
        mark_stale_dirty(found[0].stale, stores)
        return found
    found = (compose(stores, exclude_tags, model_type_of), [live_facts(path) for path, _ in stores])
    save_composed(stores[0][0], key, *found)
    return found


def mark_stale_dirty(stale: list[str], stores: Stores) -> None:
    """What reading the shards does for a stale document, done again for an index read from disk:
    the document enters the dirty set, so the next rebuild compares it."""
    from sldb.store import documents_dirty

    by_name = {name: path for path, name in stores}
    for export_id in stale:
        parts = export_id.split(":")
        link = parts[0] if len(parts) == 3 else None
        if link in by_name:
            documents_dirty.mark(by_name[link], parts[-2], parts[-1])


def with_live_stale(index: EdgeIndex, stores: Stores, facts: list, model_type_of: ModelTypeOf | None) -> EdgeIndex:
    moved = [f"{name}:{e}" if name else e for (path, name), f in zip(stores, facts) for e in stale_of_facts(path, f, model_type_of)]
    known = set(index.stale)
    extra = [e for e in dict.fromkeys(moved) if e not in known]
    return index.model_copy(update={"stale": index.stale + extra}) if extra else index

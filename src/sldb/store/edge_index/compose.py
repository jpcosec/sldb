"""Shards -> one EdgeIndex: every store's contributions merged (the same node id is one node,
the first contributor's), the cross-document rules applied. Composed once per state of the
shards: the result is kept while no shard file, and no store index, has moved."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.federation import federated_stores, qualify
from sldb.store.edge_index.resolve import resolve_edges
from sldb.store.edge_index.shard_reading import read_store_contributions
from sldb.store.edge_index.shard_signature import shards_signature
from sldb.store.models import EdgeContribution, EdgeNodeRecord, EdgeRecord

_COMPOSED: dict[tuple, tuple[tuple, EdgeIndex]] = {}


def compose_edge_index(store_path: Path, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> EdgeIndex:
    """The store's edge index, read from its shards (never rebuilt here).

    Args:
        store_path: The store's `.sldb` directory.
        include_linked: Also read the linked stores' indexes, their ids qualified by name.
        exclude_tags: Documents carrying one of these tags are left out (their nodes, their
            sections, their edges); the index itself holds everything.

    Returns:
        The composed index; shared between callers, so treat it as read-only.
    """
    stores = federated_stores(Path(store_path), include_linked)
    key = (str(stores[0][0]), include_linked, frozenset(exclude_tags))
    signature = tuple(shards_signature(path) for path, _ in stores)
    hit = _COMPOSED.get(key)
    if hit is None or hit[0] != signature:
        hit = _COMPOSED[key] = (signature, _compose(stores, frozenset(exclude_tags)))
    return hit[1]


def invalidate_composed_edge_indexes() -> None:
    """Forget every composed index (tests, or a caller that rewrote shards by hand)."""
    _COMPOSED.clear()


def _compose(stores: list[tuple[Path, str | None]], exclude_tags: frozenset[str]) -> EdgeIndex:
    nodes: dict[str, EdgeNodeRecord] = {}
    edges: list[EdgeRecord] = []
    stale: list[str] = []
    for path, name in stores:
        parts, stale_here = read_store_contributions(path, exclude_tags)
        stale += [f"{name}:{export_id}" if name else export_id for export_id in stale_here]
        _merge((qualify(p, name) for p in parts), nodes, edges)
    kept, problems = resolve_edges(nodes, edges)
    return EdgeIndex(nodes=nodes, edges=kept, problems=problems, stale=stale)


def _merge(parts: Iterable[EdgeContribution], nodes: dict[str, EdgeNodeRecord], edges: list[EdgeRecord]) -> None:
    for part in parts:
        edges += part.edges
        for node in part.nodes:
            nodes.setdefault(node.id, node)

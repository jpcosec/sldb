"""Relation-parametrized walks over a store's edge index, as library functions.

Consumers (pron's graph reader, the MCP read plane) call these instead of walking the
`EdgeIndex` themselves. Each function composes the index fresh (memoized by the shards'
own signature) and never rebuilds it.
"""

from __future__ import annotations

from typing import Iterable

from sldb.api.edges.edge_reading import load_edge_index
from sldb.store.graph import traversal as _t
from sldb.store.edge_index.node_ids import bare, kind


def _index(store, exclude_tags: Iterable[str]):
    return load_edge_index(store, include_linked=True, exclude_tags=tuple(exclude_tags))


def targets(store, node_id: str, relation: str, exclude_tags: Iterable[str] = ()) -> list[str]:
    """The unique ids an outgoing edge of `relation` points at, sorted."""
    return _t.targets(_index(store, exclude_tags), node_id, relation)


def sources(store, node_id: str, relation: str, exclude_tags: Iterable[str] = ()) -> list[str]:
    """The unique ids pointing at `node_id` through `relation`, sorted."""
    return _t.sources(_index(store, exclude_tags), node_id, relation)


def roots(store, node_type: str, relation: str, exclude_tags: Iterable[str] = ()) -> list[str]:
    """Nodes of a class with no outgoing edge of `relation`."""
    return _t.roots(_index(store, exclude_tags), node_type, relation)


def children(store, node_id: str, relation: str, exclude_tags: Iterable[str] = ()) -> list[str]:
    """The nodes pointing at `node_id` through `relation`."""
    return _t.children(_index(store, exclude_tags), node_id, relation)


def parent(store, node_id: str, relation: str, exclude_tags: Iterable[str] = ()) -> str | None:
    """The first node `node_id` points at through `relation`, or None."""
    return _t.parent(_index(store, exclude_tags), node_id, relation)


def descendants(store, node_id: str, relation: str, depth: int | None = None,
                exclude_tags: Iterable[str] = ()) -> list[str]:
    """Everything reachable following `relation` backwards, at most `depth` levels."""
    return _t.descendants(_index(store, exclude_tags), node_id, relation, depth)


def neighbors_via(store, node_id: str, out_relation: str, in_relation: str | None = None,
                  exclude_prefixes: tuple[str, ...] = (), same_kind: bool = True,
                  exclude_tags: Iterable[str] = ()) -> list[str]:
    """The nodes sharing an `out_relation` target with `node_id`, same kind by default."""
    return _t.neighbors_via(_index(store, exclude_tags), node_id, out_relation, in_relation,
                            exclude_prefixes, same_kind)


def exists(store, source: str, target: str, relation: str,
           exclude_tags: Iterable[str] = ()) -> dict | None:
    """The edge between `source` and `target`, or None."""
    return _t.exists(_index(store, exclude_tags), source, target, relation)


__all__ = [
    "bare",
    "children",
    "descendants",
    "exists",
    "kind",
    "neighbors_via",
    "parent",
    "roots",
    "sources",
    "targets",
]

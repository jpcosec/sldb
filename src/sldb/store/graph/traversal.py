"""Relation-parametrized walks over an edge index.

Every walk takes the relation name it follows; none knows which relations a world
declares. These are the primitives the old kgdb/pron graph readers implemented by hand,
now on top of `EdgeIndex`.
"""

from __future__ import annotations

from sldb.store.edge_index.node_ids import bare, kind


def targets(index, node_id: str, relation: str) -> list[str]:
    """The unique ids an outgoing edge of `relation` points at, sorted."""
    return sorted({e.target for e in index.edges_from(node_id, relation)})


def sources(index, node_id: str, relation: str) -> list[str]:
    """The unique ids pointing at `node_id` through `relation`, sorted."""
    return sorted({e.source for e in index.edges_to(node_id, relation)})


def roots(index, node_type: str, relation: str) -> list[str]:
    """Nodes of a class with no outgoing edge of `relation` (the tops of a DAG)."""
    return [n.id for n in index.nodes_of_type(node_type) if not index.edges_from(n.id, relation)]


def children(index, node_id: str, relation: str) -> list[str]:
    """The nodes pointing at `node_id` through `relation`."""
    return sources(index, node_id, relation)


def parent(index, node_id: str, relation: str) -> str | None:
    """The first node `node_id` points at through `relation`, or None."""
    found = targets(index, node_id, relation)
    return found[0] if found else None


def descendants(index, node_id: str, relation: str, depth: int | None = None) -> list[str]:
    """Everything reachable following `relation` backwards, at most `depth` levels."""
    seen: set[str] = set()
    frontier = [node_id]
    level = 0
    while frontier and (depth is None or level < depth):
        frontier = _next_level(index, frontier, relation, seen, node_id)
        level += 1
    return sorted(seen)


def _next_level(index, frontier: list[str], relation: str, seen: set[str], origin: str) -> list[str]:
    """The children of a frontier not seen yet (and never the origin)."""
    nxt: list[str] = []
    for n in frontier:
        for child in sources(index, n, relation):
            if child not in seen and child != origin:
                seen.add(child)
                nxt.append(child)
    return nxt


def neighbors_via(index, node_id: str, out_relation: str, in_relation: str | None = None,
                  exclude_prefixes: tuple[str, ...] = (), same_kind: bool = True) -> list[str]:
    """The nodes sharing an `out_relation` target with `node_id`, same kind by default."""
    back = in_relation or out_relation
    out = _shared_targets(index, node_id, out_relation, back, exclude_prefixes)
    out.discard(node_id)
    return sorted(_same_kind(out, node_id) if same_kind else out)


def _shared_targets(index, node_id: str, out_relation: str, back: str, prefixes) -> set[str]:
    """The nodes that share a target of `out_relation` with `node_id`, read back by `back`."""
    out: set[str] = set()
    for shared in targets(index, node_id, out_relation):
        if any(bare(shared).startswith(p) for p in prefixes):
            continue
        out.update(sources(index, shared, back))
    return out


def _same_kind(nodes: set[str], node_id: str) -> set[str]:
    """The subset of `nodes` whose kind matches `node_id`'s."""
    k = kind(node_id)
    return {n for n in nodes if kind(n) == k}


def exists(index, source: str, target: str, relation: str) -> dict | None:
    """The edge between `source` and `target`, or None."""
    for e in index.edges_from(source, relation):
        if e.target == target:
            return e.model_dump()
    return None

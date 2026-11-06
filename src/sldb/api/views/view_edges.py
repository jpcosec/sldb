"""The neighbour ids a section's `edges` entry adds to a row (GD25, q8).

A relation names a relation type (`edge.relation`) or a declaring field (`metadata.field` of a
`references`/`contains` edge), as a path step of the rules language does. The index's
neighbours come first, sorted, then the project graph's (GD21) for the same relation, sorted,
each a document's export id when the index tracks it and a project node id otherwise."""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import bare, kind


def row_neighbours(index: Any, graph: Any, row: dict[str, Any], edge: Any) -> list[str]:
    """The ids reached from the row along `edge.relation` in `edge.direction`."""
    found = index_neighbours(index, row["export_id"], edge.relation, edge.direction)
    for node_id in project_neighbours(index, graph, row["path"], edge.relation, edge.direction):
        if node_id not in found:
            found.append(node_id)
    return found


def index_neighbours(index: Any, export_id: str, relation: str, direction: str) -> list[str]:
    records = index.edges_from(export_id) if direction == "out" else index.edges_to(export_id)
    ends = (bare(r.target if direction == "out" else r.source) for r in records if _is_relation(r, relation))
    return sorted(set(ends))


def _is_relation(record: Any, relation: str) -> bool:
    return record.relation == relation or (record.metadata or {}).get("field") == relation


def project_neighbours(index: Any, graph: Any, path: str, relation: str, direction: str) -> list[str]:
    """The project graph's neighbours of the node at `path`, as export ids when tracked."""
    node = graph.nodes.lookup.by_path.get(path) if graph is not None else None
    if node is None:
        return []
    edges = graph.edges_from(node.id) if direction == "out" else graph.edges_to(node.id)
    ends = {e.target_id if direction == "out" else e.source_id for e in edges if e.role == relation}
    tracked = tracked_ids(index)
    return sorted({_export_id(graph, tracked, end) for end in ends})


def _export_id(graph: Any, tracked: dict[str, str], node_id: str) -> str:
    node = graph.nodes.lookup.by_id.get(node_id)
    return tracked.get(node.path, node_id) if node is not None else node_id


def tracked_ids(index: Any) -> dict[str, str]:
    """`{path: export_id}` of every document of the index."""
    return {n.semantics.get("path"): bare(n.id) for n in index.nodes.values() if kind(n.id) == "document" and n.semantics.get("path")}

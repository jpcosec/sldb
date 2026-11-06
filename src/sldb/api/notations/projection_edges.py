"""The edges between the documents a projection view selects."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _by_query(store_path: Path, selected: dict, relations: list[str], direction: str) -> set[tuple[str, str, str]]:
    """Edges of the given relation types found by a structured query."""
    from sldb.api.graph import RelationFilter, StructuredQuery, execute_query

    query = StructuredQuery(relations=[RelationFilter(relation_types=relations, direction=direction)])
    return {
        (e.source, e.target, e.relation)
        for n in execute_query(store_path, query, include_linked=False)
        for e in n.edges
        if n.id in selected and e.source in selected and e.target in selected
    }


def _by_index(store_path: Path, selected: dict) -> set[tuple[str, str, str]]:
    """All edges between selected documents, read from the edge index."""
    import sldb.api as api

    edge_index = api.load_edge_index(store_path)
    return {
        (edge.source, edge.target, edge.relation)
        for doc_id in selected
        for edge in edge_index.edges_from(doc_id)
        if edge.target in selected
    }


def collect_edges(store_path: Path, selected: dict[str, Any], relations: list[str], direction: str) -> set[tuple[str, str, str]]:
    """The `(source, target, relation)` edges among `selected`; all of them if no relations filter."""
    if relations:
        return _by_query(store_path, selected, relations, direction)
    return _by_index(store_path, selected)

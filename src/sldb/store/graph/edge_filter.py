"""Relation filtering of a node's edges."""

from __future__ import annotations


def filtered_edges(index, node_id: str, relation_filters: list) -> list:
    """The node's edges that pass the relation filters; outgoing only when no filter is given."""
    if not relation_filters:
        return index.edges_from(node_id)
    kept = [e for e in index.edges_from(node_id) if matches_any(e, relation_filters, "outgoing")]
    kept += [e for e in index.edges_to(node_id) if matches_any(e, relation_filters, "incoming")]
    return kept


def matches_any(edge, relation_filters: list, side: str) -> bool:
    """Whether one edge passes any of the filters, given its side relative to the node."""
    return any(edge_matches(edge, rf, side) for rf in relation_filters)


def edge_matches(edge, relation_filter, side: str) -> bool:
    """Whether one edge passes one filter: relation type allow-list and direction."""
    if relation_filter.relation_types and edge.relation not in relation_filter.relation_types:
        return False
    return relation_filter.direction in ("both", side)

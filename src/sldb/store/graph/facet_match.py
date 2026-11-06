"""Facet values for the executor: the payload a facet filter reads, field by field."""

from __future__ import annotations

from typing import Any


def facet_value(node, facet: str) -> object:
    """The facet payload a filter reads: identity, semantics, a document's projected payload, or
    a carried facet."""
    if facet == "identity":
        return {"node_id": node.id, "node_type": node.node_type}
    if facet == "semantics":
        return node.semantics
    if facet == "payload":
        return node.payload
    return node.facets.get(facet)


def resolve_field(value: object, field: str) -> Any:
    """Read a field from a facet payload: dict, list, or attribute-addressable object."""
    if value is None:
        return None
    if isinstance(value, list):
        return first_field(value, field)
    return read_field(value, field)


def first_field(values: list, field: str) -> Any:
    """The first non-null field value across a list payload."""
    for item in values:
        resolved = read_field(item, field)
        if resolved is not None:
            return resolved
    return None


def read_field(value: object, field: str) -> Any:
    """Read one field from a dict or attribute-addressable object."""
    if isinstance(value, dict):
        return value.get(field)
    return getattr(value, field, None)

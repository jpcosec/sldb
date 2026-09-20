"""Facet and condition matching for the executor."""

from __future__ import annotations

from typing import Any


def matches_filters(node, filters: list) -> bool:
    """Whether a node matches every facet filter of a query."""
    return all(facet_matches(node, facet_filter) for facet_filter in filters)


def facet_matches(node, facet_filter) -> bool:
    """Whether a node matches every condition of one facet filter."""
    value = facet_value(node, facet_filter.facet)
    return all(condition_matches(value, condition) for condition in facet_filter.conditions)


def facet_value(node, facet: str) -> object:
    """The facet payload a filter reads: identity, semantics, or a carried facet."""
    if facet == "identity":
        return {"node_id": node.id, "node_type": node.node_type}
    if facet == "semantics":
        return node.semantics
    return node.facets.get(facet)


def condition_matches(value: object, condition) -> bool:
    """Whether one facet field value satisfies one FieldCondition."""
    if condition.op == "is_null":
        return resolve_field(value, condition.field) is None
    if condition.op == "is_not_null":
        return resolve_field(value, condition.field) is not None
    return ordered_compare(resolve_field(value, condition.field), condition)


def ordered_compare(actual: Any, condition) -> bool:
    """Evaluate the value-comparing operators that are not the null ones."""
    if condition.op == "eq":
        return actual == condition.value
    if condition.op == "ne":
        return actual != condition.value
    if condition.op == "contains":
        return isinstance(actual, list) and condition.value in actual
    if condition.op == "starts_with":
        return isinstance(actual, str) and actual.startswith(condition.value)
    return ordered_magnitude(actual, condition)


def ordered_magnitude(actual: Any, condition) -> bool:
    """Evaluate the greater-than and less-than operators."""
    if condition.op == "gt":
        return actual is not None and actual > condition.value
    if condition.op == "lt":
        return actual is not None and actual < condition.value
    return False


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

"""Facet filters of a `StructuredQuery`, evaluated by the predicate language (GO05).

Each `FieldCondition` is translated to the language (`FieldCondition.predicate()`, rules-
language.md §7) and evaluated on the facet's fields; a null value is an absent field, as in a
projection (GO04). On the `payload` facet (a document node's projected fields): an absent
field only satisfies `is_null`; a list's `contains` is membership and its `eq`/`ne` compare
the whole list (Python equality, no coercion); a comparison Python cannot make is false. Only
document nodes carry the facet: any other node matches no payload filter.
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import kind
from sldb.store.graph.facet_match import facet_value, resolve_field
from sldb.store.graph.language.predicate_documents import payload_holds

PAYLOAD = "payload"


def filters_hold(node, filters: list) -> bool:
    """Whether a node matches every facet filter of a query."""
    return all(_filter_holds(node, facet_filter) for facet_filter in filters)


def payload_matches(node, facet_filter) -> bool:
    """Whether a document node's projection satisfies every condition of the filter."""
    if kind(node.id) != "document":
        return False
    return all(payload_condition(node.payload, condition) for condition in facet_filter.conditions)


def payload_condition(payload: dict, condition) -> bool:
    """One FieldCondition over a projected payload, through the language."""
    present = {key: value for key, value in payload.items() if value is not None}
    return payload_holds(condition.predicate(), present)


def unprojected_fields(payload_fields: dict[str, list[str]], filters: list) -> list[str]:
    """Fields a payload filter names that no model projects, in the order named."""
    known = {f for fields in payload_fields.values() for f in fields}
    named = [c.field for f in filters if f.facet == PAYLOAD for c in f.conditions]
    return [f for f in dict.fromkeys(named) if f not in known]


def _filter_holds(node, facet_filter) -> bool:
    if facet_filter.facet == PAYLOAD:
        return payload_matches(node, facet_filter)
    value = facet_value(node, facet_filter.facet)
    return all(payload_condition(_field_of(value, c.field), c) for c in facet_filter.conditions)


def _field_of(value: Any, field: str) -> dict[str, Any]:
    return {field: resolve_field(value, field)}

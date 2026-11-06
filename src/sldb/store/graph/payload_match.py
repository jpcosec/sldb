"""Conditions on the `payload` facet (GO04): a document node's projected fields.

The facet's operators keep `facet_match`'s meaning, with what a projection adds: on a null (an
absent field) only `is_null` / `is_not_null` decide, the others are false; on a list,
`contains` is membership, `eq` / `ne` compare the whole list (Python equality, no coercion),
`gt` / `lt` / `starts_with` are false, `is_null` false and `is_not_null` true. A comparison
Python cannot order (`"a" > 1`) is false, not an error. Only document nodes carry the facet:
any other node matches no payload filter.
"""

from __future__ import annotations

from sldb.store.edge_index.node_ids import kind
from sldb.store.graph.facet_match import condition_matches, ordered_compare

PAYLOAD = "payload"
_NULL_OPS = ("is_null", "is_not_null")


def payload_matches(node, facet_filter) -> bool:
    """Whether a document node's projection satisfies every condition of the filter."""
    if kind(node.id) != "document":
        return False
    return all(payload_condition(node.payload, condition) for condition in facet_filter.conditions)


def payload_condition(payload: dict, condition) -> bool:
    """One FieldCondition over a projected payload."""
    if condition.op in _NULL_OPS:
        return condition_matches(payload, condition)
    actual = payload.get(condition.field)
    if actual is None or (isinstance(actual, list) and condition.op in ("gt", "lt")):
        return False
    try:
        return ordered_compare(actual, condition)
    except TypeError:
        return False


def unprojected_fields(payload_fields: dict[str, list[str]], filters: list) -> list[str]:
    """Fields a payload filter names that no model projects, in the order named."""
    known = {f for fields in payload_fields.values() for f in fields}
    named = [c.field for f in filters if f.facet == PAYLOAD for c in f.conditions]
    return [f for f in dict.fromkeys(named) if f not in known]

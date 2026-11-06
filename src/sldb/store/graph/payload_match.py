"""Facet filters of a `StructuredQuery`, evaluated by the predicate language.

Each filter's `where` is a predicate (rules-language.md) over the facet's fields, without
paths: a quantifier or a `count` is `SLDBGraphArgumentError` naming it. A null value is an
absent field, as in a projection (GO04). On the `payload` facet (a document node's projected
fields) the predicate reads the projection; a list's `in` is membership and `=`/`!=` compare
the whole list (Python equality, no coercion); a comparison Python cannot make is false. Only
document nodes carry the facet: any other node matches no payload filter.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from sldb.store.edge_index.node_ids import kind
from sldb.store.exceptions import SLDBGraphArgumentError
from sldb.store.graph.facet_match import facet_value, resolve_field
from sldb.store.graph.language.predicate_api import as_predicate
from sldb.store.graph.language.predicate_ast import Predicate, leaf_fields, walk
from sldb.store.graph.language.predicate_documents import payload_holds

PAYLOAD = "payload"


def filters_hold(node, filters: list) -> bool:
    """Whether a node matches every facet filter of a query."""
    return all(_filter_holds(node, facet_filter) for facet_filter in filters)


def payload_matches(node, facet_filter) -> bool:
    """Whether a document node's projection satisfies the filter's predicate."""
    if kind(node.id) != "document":
        return False
    return where_holds(facet_filter.where, node.payload)


def where_holds(where: str, values: dict) -> bool:
    """Whether a facet predicate holds on some field values (`None` is an absent field)."""
    present = {key: value for key, value in values.items() if value is not None}
    return payload_holds(facet_predicate(where), present)


@lru_cache(maxsize=256)
def facet_predicate(where: str) -> Predicate | str:
    """The parsed predicate of a facet filter (`""` stays empty: no condition); a path is
    rejected (SLDBGraphArgumentError) and text that does not parse is WherePredicateError."""
    if not where.strip():
        return ""
    parsed = as_predicate(where)
    paths = [n[1] for n in walk(parsed.root) if n[0] in ("quant", "count")]
    if paths:
        raise SLDBGraphArgumentError(f"facet filter where {where!r}: a path does not apply to a facet ({', '.join(paths)})")
    return parsed


def where_fields(where: str) -> list[str]:
    """The fields a facet predicate names, in order, without repeats."""
    parsed = facet_predicate(where)
    return leaf_fields(parsed.root) if isinstance(parsed, Predicate) else []


def unprojected_fields(payload_fields: dict[str, list[str]], filters: list) -> list[str]:
    """Fields a payload filter names that no model projects, in the order named."""
    known = {f for fields in payload_fields.values() for f in fields}
    named = [name for f in filters if f.facet == PAYLOAD for name in where_fields(f.where)]
    return [f for f in dict.fromkeys(named) if f not in known]


def _filter_holds(node, facet_filter) -> bool:
    if facet_filter.facet == PAYLOAD:
        return payload_matches(node, facet_filter)
    value = facet_value(node, facet_filter.facet)
    return where_holds(facet_filter.where, _fields_of(value, where_fields(facet_filter.where)))


def _fields_of(value: Any, fields: list[str]) -> dict[str, Any]:
    return {field: resolve_field(value, field) for field in fields}

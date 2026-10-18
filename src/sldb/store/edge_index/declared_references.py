"""What a document's declared reference fields contribute: one `references` or `contains`
edge per id held in a field the model declared.

A model declares which of its fields hold document ids:

    __references__ = ["about"]                  # a reference to another document
    __containment__ = {"steps": ["StepDoc"]}    # a child, restricted to those models

Those two dunders were readable metadata only: `/schema` and `fields_routes` exposed them
and the edge index ignored them. Everything else the model declares already reaches the
graph -- `model_fields` becomes `has_field`, `base_models` becomes `extends`, `__semantics__`
becomes `tagged_as` -- so a declared reference was the one declaration that did not.

These edges are `origin: "schema"`, like `has_field` and `extends`. A shard records each
value as written (`declared`) with the models the field allows (`__containment__`, or
`__reference_models__ = {"depends_on": ["TaskDoc"]}` for a reference field); which document
it names is decided when the index is composed (`declared_resolution`), since a bare id or a
path depends on what else is tracked. One that names nothing is reported there, apart from
the authored-edge problems: a declared reference is a shape, not an assertion.
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.records import edge
from sldb.store.models import EdgeRecord

Payload = dict[str, Any]

CONTAINS = "contains"
REFERENCES = "references"
#: Where a declared value that is not an export id points until the index is composed.
PENDING_TARGET = "sldb://unresolved_ref/"


def declared_reference_edges(model_name: str, doc_name: str, model_type: Any | None, payload: Payload | None) -> list[EdgeRecord]:
    """The edges the model's `__references__` and `__containment__` declare for this document.

    Args:
        model_name: Model the document is tracked under.
        doc_name: The document's name, used for its own node id.
        model_type: The imported model class, or None when it cannot be imported (a linked
            store's model): nothing is declared then, as in `build_model_edges`.
        payload: The document's extracted payload, or None when it cannot be read.

    Returns:
        One edge per id found, `contains` for containment fields and `references` for the
        rest. Order follows the declaration, then the order of ids inside each field.
    """
    if model_type is None or payload is None:
        return []
    source = doc_node_id(f"{model_name}:{doc_name}")
    containment: dict[str, list[str]] = getattr(model_type, "__containment__", {}) or {}
    allowed_refs: dict[str, list[str]] = getattr(model_type, "__reference_models__", {}) or {}
    references = list(getattr(model_type, "__references__", []) or []) + [f for f in allowed_refs if f not in (getattr(model_type, "__references__", []) or [])]
    contained = [(field, CONTAINS, list(allowed)) for field, allowed in containment.items()]
    # Containment already spoke for a field declared both ways.
    referenced = [(field, REFERENCES, list(allowed_refs.get(field, []))) for field in references if field not in containment]
    return [e for field, relation, allowed in contained + referenced for e in _field_edges(source, payload, field, relation, allowed)]


def _field_edges(source: str, payload: Payload, field: str, relation: str, allowed: list[str]) -> list[EdgeRecord]:
    """One edge per value in `field` that can name a document; the field may hold one or a list."""
    extra = {"allowed_models": allowed} if allowed else {}
    return [
        edge(source, _target(value), relation, "schema", field=field, declared=value, **extra)
        for value in _values_in(payload.get(field))
        if is_export_id(value) or allowed or relation == CONTAINS or looks_like_path(value)
    ]


def _target(value: str) -> str:
    """An export id points at its document now; anything else waits for the composed index."""
    return doc_node_id(value) if is_export_id(value) else PENDING_TARGET + value


def _values_in(value: Any) -> list[str]:
    raw = value if isinstance(value, list) else [value]
    return [v for v in (item.strip().strip("`").strip() for item in raw if isinstance(item, str)) if v]


def is_export_id(value: str) -> bool:
    """`Model:name` (or `store:Model:name`); a URL is not one."""
    return ":" in value and "://" not in value


def looks_like_path(value: str) -> bool:
    return "/" in value or value.endswith(".md")

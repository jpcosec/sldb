"""What a document's declared reference fields contribute: one `references` or `contains`
edge per id held in a field the model declared.

A model declares which of its fields hold document ids:

    __references__ = ["about"]                  # a reference to another document
    __containment__ = {"steps": ["StepDoc"]}    # a child, restricted to those models

Those two dunders were readable metadata only: `/schema` and `fields_routes` exposed them
and the edge index ignored them. Everything else the model declares already reaches the
graph -- `model_fields` becomes `has_field`, `base_models` becomes `extends`, `__semantics__`
becomes `tagged_as` -- so a declared reference was the one declaration that did not.

These edges are `origin: "schema"`, like `has_field` and `extends`: a reference to an
untracked document is dropped by `resolve_edges` instead of reported, because the model
declared a shape, not an authored assertion. An authored edge that dangles is a `RelationDoc`
problem; a declared one is just a field whose target is not in this store.
"""

from __future__ import annotations

from typing import Any

from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.edge_index.records import edge
from sldb.store.models import EdgeRecord

Payload = dict[str, Any]

CONTAINS = "contains"
REFERENCES = "references"


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
    references: list[str] = getattr(model_type, "__references__", []) or []
    contained = [(field, CONTAINS, list(allowed)) for field, allowed in containment.items()]
    # Containment already spoke for a field declared both ways.
    referenced = [(field, REFERENCES, []) for field in references if field not in containment]
    return [e for field, relation, allowed in contained + referenced for e in _field_edges(source, payload, field, relation, allowed)]


def _field_edges(source: str, payload: Payload, field: str, relation: str, allowed: list[str]) -> list[EdgeRecord]:
    """One edge per id in `field`; the field may hold one id or a list of them."""
    return [
        edge(source, doc_node_id(target), relation, "schema", field=field, **({"allowed_models": allowed} if allowed else {}))
        for target in _ids_in(payload.get(field))
    ]


def _ids_in(value: Any) -> list[str]:
    """The export ids held in a field value.

    A declared id is written `Model:name`: the bare name is ambiguous across models and
    cannot be resolved to a node here, so it is left out rather than guessed at.
    """
    raw = value if isinstance(value, list) else [value]
    return [item.strip() for item in raw if isinstance(item, str) and ":" in item.strip()]

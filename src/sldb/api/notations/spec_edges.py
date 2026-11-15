"""`spec_edges`: las aristas de un spec, por tipo de diagrama.

Migrado de `spec2viz.sldb_sync` (`spec_edges`, `_edge_label`, `_edge_attributes`).
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.spec_activity import activity_edges
from sldb.api.notations.spec_matrix import matrix_edges
from sldb.api.notations.spec_refs import plain, relation_token
from sldb.api.notations.spec_sync_constants import (
    _DEPLOYMENT_RELATIONS,
    _EDGE_ATTRIBUTE_FIELDS,
    _EDGE_COLLECTIONS,
    _EDGE_LABEL_FIELDS,
    _MESSAGE_RELATIONS,
)

_DERIVED = {"activity": activity_edges, "component_view_matrix": matrix_edges}


def _edge_label(raw: dict) -> str:
    """`notes` del RelationDoc: etiqueta, `[guarda]` y `/ accion` como en un statechart."""
    label = next((str(raw[f]) for f in _EDGE_LABEL_FIELDS if raw.get(f)), "")
    if raw.get("guard"):
        label = f"{label} [{raw['guard']}]".strip()
    if raw.get("action"):
        label = f"{label} / {raw['action']}".strip(" /")
    return label


def _edge_attributes(diagram_type: str, raw: dict) -> dict[str, Any]:
    return {f: plain(raw[f]) for f in _EDGE_ATTRIBUTE_FIELDS.get(diagram_type, ()) if raw.get(f) not in (None, "")}


def _edge_relation(diagram_type: str, raw: dict, relation_field: str | None, default: str) -> str:
    """La relacion de la arista como token; secuencia y despliegue tienen su propia tabla."""
    value = raw.get(relation_field) if relation_field else None
    if diagram_type == "sequence":
        return _MESSAGE_RELATIONS.get(str(value or "").strip().lower(), relation_token(value, default))
    if diagram_type == "deployment":
        return _DEPLOYMENT_RELATIONS.get(str(raw.get("kind") or ""), default)
    return relation_token(value, default)


def _edge(diagram_type: str, raw: dict, relation_field: str | None, default: str) -> dict:
    condition = str(raw.get("condition") or "") if diagram_type == "sequence" else ""
    relation = _edge_relation(diagram_type, raw, relation_field, default)
    return {"from": str(raw["from"]), "to": str(raw["to"]), "relation": relation, "label": _edge_label(raw), "condition": condition,
            "attributes": _edge_attributes(diagram_type, raw)}


def spec_edges(spec: dict) -> list[dict]:
    """Las aristas del spec en orden: from, to, relation (token), label (con guarda y accion), condition y attributes."""
    data = spec.get("data") or {}
    diagram_type = str(spec.get("type"))
    if diagram_type in _DERIVED:
        return _DERIVED[diagram_type](data)
    entry = _EDGE_COLLECTIONS.get(diagram_type)
    if entry is None:
        return []
    collection, relation_field, default = entry
    edges = [raw for raw in data.get(collection) or [] if isinstance(raw, dict) and raw.get("from") and raw.get("to")]
    return [_edge(diagram_type, raw, relation_field, default) for raw in edges]

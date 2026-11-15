"""`spec_elements`: los elementos de un spec, por tipo de diagrama.

Migrado de `spec2viz.sldb_sync.spec_elements`.
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.spec_activity import activity_pseudonodes
from sldb.api.notations.spec_element import element, pairs
from sldb.api.notations.spec_matrix import matrix_elements
from sldb.api.notations.spec_sync_constants import _ELEMENT_COLLECTIONS_SYNC


def _initial_flags(diagram_type: str, data: dict) -> dict[str, dict[str, Any]]:
    """El estado inicial de un diagrama de estados, marcado con `initial: true`."""
    if diagram_type == "state" and data.get("initial"):
        return {str(data["initial"]): {"initial": True}}
    return {}


def spec_elements(spec: dict) -> list[dict]:
    """Los elementos del spec: id, label, kind, collection, contains, atoms, refs, description y data.

    `data` es el resto del elemento; ademas `initial`/`final` marcan el estado o paso inicial y
    final (state, activity) y las etapas de una matriz llevan `view` y `order`.
    """
    data = spec.get("data") or {}
    diagram_type = str(spec.get("type"))
    if diagram_type == "component_view_matrix":
        return matrix_elements(data)
    flags = _initial_flags(diagram_type, data)
    collections = _ELEMENT_COLLECTIONS_SYNC.get(diagram_type, ())
    out = [element(eid, el, c, flags.get(str(eid))) for c in collections for eid, el in pairs(data.get(c) or {}) if eid]
    if diagram_type == "activity":
        out.extend(activity_pseudonodes(data, {e["id"] for e in out}))
    return out

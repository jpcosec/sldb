"""Elementos y aristas de una matriz componente-vista (`component_view_matrix`).

Migrado de `spec2viz.sldb_sync` (`_matrix_elements`, `_matrix_edges`).
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.spec_element import element
from sldb.api.notations.spec_refs import stage_id


def _stage_element(view: dict, stage: dict, order: int) -> dict:
    """Una etapa de una vista: `collection: stages`, con `view`, `view_label` y `order`."""
    vid = str(view["id"])
    flags = {"view": vid, "view_label": str(view.get("label") or view["id"]), "order": order}
    return element(stage_id(vid, str(stage["id"])), {"label": stage.get("label") or stage["id"]}, "stages", flags)


def _stage_elements(data: dict) -> list[dict]:
    """Las etapas de cada vista, en orden."""
    out: list[dict] = []
    for view in data.get("views") or []:
        if not isinstance(view, dict) or not view.get("id"):
            continue
        for order, stage in enumerate(view.get("stages") or [], start=1):
            if isinstance(stage, dict) and stage.get("id"):
                out.append(_stage_element(view, stage, order))
    return out


def _component_elements(components: Any, out: list[dict]) -> list[dict]:
    """Los componentes, anidados por `children` -> contains."""
    for comp in components or []:
        if not isinstance(comp, dict) or not comp.get("name"):
            continue
        children = [c for c in comp.get("children") or [] if isinstance(c, dict) and c.get("name")]
        el = element(comp["name"], {k: v for k, v in comp.items() if k != "children"}, "components")
        el["contains"] = [str(c["name"]) for c in children]
        out.append(el)
        _component_elements(children, out)
    return out


def matrix_elements(data: dict) -> list[dict]:
    """Componentes (anidados por `children` -> contains) y etapas por vista (`collection: stages`)."""
    stages = _stage_elements(data)
    return stages + _component_elements(data.get("components"), [])


def _occupies(comp: dict) -> list[dict]:
    """Un `occupies` por etapa de cada vista del componente; la vista va en la etiqueta."""
    return [
        {"from": str(comp["name"]), "to": stage_id(str(view_id), str(stage)), "relation": "occupies", "label": str(view_id),
         "condition": "", "attributes": {"view": str(view_id), "stage": str(stage)}}
        for view_id, stages in (comp.get("stages") or {}).items() for stage in stages or []
    ]


def _component_edges(components: Any, out: list[dict]) -> list[dict]:
    for comp in components or []:
        if not isinstance(comp, dict) or not comp.get("name"):
            continue
        out.extend(_occupies(comp))
        _component_edges(comp.get("children"), out)
    return out


def matrix_edges(data: dict) -> list[dict]:
    """Un `occupies` por componente y etapa de cada vista; la vista va en la etiqueta."""
    return _component_edges(data.get("components"), [])

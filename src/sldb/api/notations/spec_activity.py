"""Pseudonodos y aristas de un diagrama de actividad.

Migrado de `spec2viz.sldb_sync` (`_activity_pseudonodes`, `_pseudonode`, `_activity_edges`).
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.spec_element import element
from sldb.api.notations.spec_sync_constants import ACTIVITY_FINAL, ACTIVITY_INITIAL


def activity_pseudonodes(data: dict, steps: set[str]) -> list[dict]:
    """El inicial propio y el final: el propio `end` si no es un paso, uno aparte si lo es."""
    out: list[dict] = []
    if data.get("start"):
        out.append(_pseudonode(ACTIVITY_INITIAL, "start", {"initial": True}))
    end = str(data.get("end") or "")
    if end:
        out.append(_pseudonode(ACTIVITY_FINAL if end in steps else end, "end", {"final": True}))
    return out


def _pseudonode(eid: str, kind: str, flags: dict[str, Any]) -> dict:
    # el titulo es `start`/`end` (SpecNodeDoc lo exige); los glifos start y end no lo muestran
    return element(eid, {"kind": kind, "label": kind}, "steps", flags)


def _flow(source: str, target: str, relation: str = "next", label: str = "") -> dict:
    """Una arista `next` o una rama `branch` (con su etiqueta en attributes)."""
    attributes = {"branch": label} if relation == "branch" else {}
    return {"from": source, "to": target, "relation": relation, "label": label, "condition": "", "attributes": attributes}


def _step_edges(sid: Any, step: dict) -> list[dict]:
    """`next` -> relacion `next`; cada rama de `branches` -> relacion `branch` con su etiqueta."""
    out = [_flow(str(sid), str(step["next"]))] if step.get("next") else []
    return out + [_flow(str(sid), str(target), "branch", str(label)) for label, target in (step.get("branches") or {}).items()]


def activity_edges(data: dict) -> list[dict]:
    """Las aristas de los pasos, mas las de los pseudonodos: el inicial al paso de `start` y,
    cuando `end` es un paso, ese paso al final."""
    steps = data.get("steps") or {}
    out = [_flow(ACTIVITY_INITIAL, str(data["start"]))] if data.get("start") else []
    for sid, step in steps.items():
        if isinstance(step, dict):
            out.extend(_step_edges(sid, step))
    end = str(data.get("end") or "")
    if end and end in steps:
        out.append(_flow(end, ACTIVITY_FINAL))
    return out

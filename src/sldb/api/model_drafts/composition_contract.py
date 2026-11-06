"""Check that a model's compositions name known source fields and have render markers."""

from __future__ import annotations

from typing import Any

from sldb.core.exceptions import SLDBModelEditError


def check_composition_contract(label: str, model_type: Any, names: set[str]) -> None:
    """Refuse a composition that is not a dict, cites an unknown field or lacks its marker."""
    template = str(getattr(model_type, "__template__", "") or "")
    for comp_name, spec in (getattr(model_type, "__compositions__", {}) or {}).items():
        if not isinstance(spec, dict):
            raise SLDBModelEditError(f"{label}: composition '{comp_name}' must be a dictionary.")
        src = spec.get("source_field")
        if not src or src not in names:
            raise SLDBModelEditError(f"{label}: composition '{comp_name}' references unknown source field '{src}'.")
        if f"⸢render•{comp_name}⸥" not in template:
            raise SLDBModelEditError(f"{label}: composition '{comp_name}' missing render marker '⸢render•{comp_name}⸥' in template.")

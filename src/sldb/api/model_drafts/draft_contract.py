"""Check that a model's template only references fields the model declares.

Moved here from `sldb.cli.commands.models_validate_utils`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any

from sldb.core.exceptions import SLDBModelEditError
from sldb.runtime.validation import Validator


def validate_template_contract(model_type: Any) -> None:
    """Refuse a model whose template markers name fields the model does not declare,
    or whose references, containment, or compositions target unknown fields, or whose
    compositions lack render markers in __template__.

    Raises:
        SLDBModelEditError: When any referenced field is unknown or a composition marker is missing.
    """
    recipes = Validator(model_type)._get_recipes()
    field_names = set(model_type.model_fields)
    referenced = _extract_referenced_fields(recipes)
    unknown = sorted(name for name in referenced if name not in field_names)
    if unknown:
        raise SLDBModelEditError(f"Draft for '{model_type.__name__}' references unknown fields: {', '.join(unknown)}")

    references = getattr(model_type, "__references__", []) or []
    unknown_refs = sorted(r for r in references if r not in field_names)
    if unknown_refs:
        raise SLDBModelEditError(f"Draft for '{model_type.__name__}': __references__ references unknown field(s): {', '.join(unknown_refs)}")

    containment = getattr(model_type, "__containment__", {}) or {}
    unknown_cont = sorted(k for k in containment if k not in field_names)
    if unknown_cont:
        raise SLDBModelEditError(f"Draft for '{model_type.__name__}': __containment__ references unknown field(s): {', '.join(unknown_cont)}")

    compositions = getattr(model_type, "__compositions__", {}) or {}
    template_str = str(getattr(model_type, "__template__", "") or "")
    for comp_name, comp_spec in compositions.items():
        if not isinstance(comp_spec, dict):
            raise SLDBModelEditError(f"Draft for '{model_type.__name__}': composition '{comp_name}' must be a dictionary.")
        src_field = comp_spec.get("source_field")
        if not src_field or src_field not in field_names:
            raise SLDBModelEditError(f"Draft for '{model_type.__name__}': composition '{comp_name}' references unknown source field '{src_field}'.")
        if f"⸢render•{comp_name}⸥" not in template_str:
            raise SLDBModelEditError(f"Draft for '{model_type.__name__}': composition '{comp_name}' missing render marker '⸢render•{comp_name}⸥' in template.")


def _extract_referenced_fields(recipes: list[Any]) -> set[str]:
    """Every field name the template's recipes mark, including table column markers."""
    referenced: set[str] = set()
    for recipe in recipes:
        markers = list(recipe.get("props_info", []))
        if "marker" in recipe:
            markers.append(recipe["marker"])
        if "col_markers" in recipe:
            for marker_info in recipe["col_markers"].values():
                markers.append(marker_info["marker"])
        _add_marker_names(markers, referenced)
    return referenced


def _add_marker_names(markers: list[Any], referenced: set[str]) -> None:
    """Collect the names of markers given as objects or dicts."""
    for marker in markers:
        name = getattr(marker, "name", None)
        if isinstance(marker, dict):
            name = marker.get("name")
        if name:
            referenced.add(name)

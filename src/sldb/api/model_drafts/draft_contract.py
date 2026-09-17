"""Check that a model's template only references fields the model declares.

Moved here from `sldb.cli.commands.models_validate_utils`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any

from sldb.core.exceptions import SLDBModelEditError
from sldb.runtime.validation import Validator


def validate_template_contract(model_type: Any) -> None:
    """Refuse a model whose template markers name fields the model does not declare.

    Raises:
        SLDBModelEditError: Listing the unknown field names.
    """
    recipes = Validator(model_type)._get_recipes()
    field_names = set(model_type.model_fields)
    referenced = _extract_referenced_fields(recipes)
    unknown = sorted(name for name in referenced if name not in field_names)
    if unknown:
        raise SLDBModelEditError(f"Draft for '{model_type.__name__}' references unknown fields: {', '.join(unknown)}")


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

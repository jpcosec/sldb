"""Check that a model's template only references fields the model declares.

Moved here from `sldb.cli.commands.models_validate_utils`, which re-exports these names.
"""

from __future__ import annotations

from typing import Any

from sldb.api.model_drafts.composition_contract import check_composition_contract
from sldb.core.exceptions import SLDBModelEditError
from sldb.runtime.validation import Validator


def validate_template_contract(model_type: Any) -> None:
    """Refuse a model whose template markers name fields the model does not declare,
    or whose references, containment, or compositions target unknown fields, or whose
    compositions lack render markers in __template__.

    Raises:
        SLDBModelEditError: When any referenced field is unknown or a composition marker is missing.
    """
    names = set(model_type.model_fields)
    label = f"Draft for '{model_type.__name__}'"
    unknown = sorted(n for n in _extract_referenced_fields(Validator(model_type)._get_recipes()) if n not in names)
    if unknown:
        raise SLDBModelEditError(f"{label} references unknown fields: {', '.join(unknown)}")
    for attr in ("__references__", "__containment__"):
        _check_known_fields(label, attr, getattr(model_type, attr, None) or [], names)
    check_composition_contract(label, model_type, names)


def _check_known_fields(label: str, attr: str, cited: Any, names: set[str]) -> None:
    """Every field an attribute (references or containment keys) cites must be declared."""
    unknown = sorted(f for f in cited if f not in names)
    if unknown:
        raise SLDBModelEditError(f"{label}: {attr} references unknown field(s): {', '.join(unknown)}")


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

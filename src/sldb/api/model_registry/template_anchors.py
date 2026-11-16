"""The literal paragraph that anchors each field of a model's template.

A template like ``## Goal\\n\\n_Describe the goal._\\n\\n⸢rev,markdown•goal⸥`` carries a
placeholder paragraph that render writes and extract consumes as the anchor of ``goal``.
Consumers (deskops) need that text to tell a placeholder from a value; they used to read it
from sldb's internals. This reads it from the same recipes ``Validator(model).extract`` uses.
"""

from __future__ import annotations

import re
from typing import Any

from sldb.models.structured_doc import StructuredNLDoc
from sldb.runtime.validation import _recipes


def template_anchors(model_type: type[StructuredNLDoc]) -> dict[str, str]:
    """Map each field whose marker follows a literal paragraph to that paragraph's text.

    The anchor is the extractor's ``anchor`` recipe of a paragraph block immediately before
    the field's block (same section: a heading in between is a block of its own). The text is
    the paragraph as the template writes it, italic delimiters included, without trailing
    spaces. Fields without such a paragraph are absent.
    """
    if not (isinstance(model_type, type) and issubclass(model_type, StructuredNLDoc)):
        raise TypeError(f"template_anchors expects a StructuredNLDoc subclass, got {model_type!r}")
    recipes = _recipes(model_type.__template__)
    anchors: dict[str, str] = {}
    for previous, recipe in zip(recipes, recipes[1:]):
        if not _is_paragraph_anchor(previous) or recipe["outer_index"] != previous["outer_index"] + 1:
            continue
        for name in _field_names(recipe):
            anchors.setdefault(name, _anchor_text(previous))
    return anchors


def _is_paragraph_anchor(recipe: dict[str, Any]) -> bool:
    return bool(recipe.get("anchor")) and recipe.get("outer_type") == "paragraph" and recipe.get("regex") != "^$"


def _field_names(recipe: dict[str, Any]) -> list[str]:
    markers = list(recipe.get("props_info", []))
    if "marker" in recipe:
        markers.append(recipe["marker"])
    markers.extend(item["marker"] for item in recipe.get("markers", []))
    names = (m.get("name") if isinstance(m, dict) else getattr(m, "name", None) for m in markers)
    return [name for name in names if name]


def _anchor_text(recipe: dict[str, Any]) -> str:
    """The anchor recipe keeps the paragraph as ``^re.escape(text)$``; undo the escape."""
    return re.sub(r"\\(.)", r"\1", recipe["regex"][1:-1], flags=re.S).rstrip()

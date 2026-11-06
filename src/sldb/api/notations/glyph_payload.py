"""The `GlyphDoc` payload a notation sync writes."""

from __future__ import annotations

from typing import Any

from sldb.notations.notation import notation_ref


def _head(notation: Any, glyph: Any) -> dict[str, Any]:
    """Identity and matching rule of the glyph."""
    return {
        "id": f"{notation.name}.{glyph.id}",
        "title": glyph.title or glyph.id,
        "notation": notation_ref(notation.name),
        "model": glyph.model,
        "where": glyph.where,
    }


def _drawing(glyph: Any) -> dict[str, Any]:
    """How the glyph draws a node."""
    form = f'(where {glyph.model} "{glyph.where}")' if glyph.where else f"(model {glyph.model})"
    return {
        "shape": glyph.shape, "label": glyph.label, "label_style": glyph.label_style, "keyword": glyph.keyword,
        "compartments": list(glyph.compartments), "function": glyph.function,
        "form": glyph.form or form, "description": glyph.description,
    }


def glyph_payload(notation: Any, glyph: Any) -> dict[str, Any]:
    """The `GlyphDoc` payload of one glyph of `notation`."""
    return {
        **_head(notation, glyph),
        **_drawing(glyph),
        "kind": glyph.kind or None,
        "fill": glyph.fill or None,
        "stroke": glyph.stroke or None,
        "icon": glyph.icon or None,
    }

"""Payloads of the NotationDoc, PaletteDoc and RelationTypeDoc a sync writes."""

from __future__ import annotations

from typing import Any

from sldb.notations.notation import glyph_ref, link_ref
from sldb.notations.palette import palette_ref


def relation_type_payload(relation: str, description: str) -> dict[str, Any]:
    """A directed many-to-many `RelationTypeDoc` for `relation`."""
    return {
        "title": relation, "name": relation, "direction": "directed", "cardinality": "many_to_many",
        "axis": "", "source_types": [], "target_types": [], "condition": "", "description": description,
    }


def palette_payload(palette: Any) -> dict[str, Any]:
    """The `PaletteDoc` payload of a loaded palette."""
    return {
        "id": palette.name,
        "name": palette.name,
        "title": palette.title or palette.name,
        "backgrounds": palette.backgrounds.model_dump(),
        "ink": palette.ink.model_dump(),
        "icon_set": palette.icon_set.model_dump(),
        **{key: {k: v.model_dump() for k, v in getattr(palette, key).items()} for key in ("colors", "kinds")},
        "description": palette.description,
    }


def _notation_head(notation: Any) -> dict[str, Any]:
    """Identity and kind of the notation."""
    return {
        "id": notation.name,
        "title": notation.title or notation.name,
        "name": notation.name,
        "diagram_type": notation.diagram_type,
        "level": notation.level,
        "projection": notation.projection,
    }


def notation_payload(notation: Any, palette: Any) -> dict[str, Any]:
    """The `NotationDoc` payload: layout, markers and refs to its glyphs, links and palette."""
    return {
        **_notation_head(notation),
        "layout": dict(notation.layout),
        "markers": [m.model_dump() for m in notation.markers],
        "glyphs": [glyph_ref(notation.name, g.id) for g in notation.glyphs],
        "links": [link_ref(notation.name, l.id) for l in notation.links],
        "palette": palette_ref(palette.name) if palette is not None else None,
        "description": notation.description,
    }

"""Fachada de notaciones: el vocabulario visual de un tipo de diagrama como datos."""

from __future__ import annotations

from sldb.notations.diagram_type import DiagramType
from sldb.notations.glyph_spec import GlyphSpec
from sldb.notations.link_end_spec import LinkEndSpec
from sldb.notations.link_spec import LinkSpec
from sldb.notations.marker_spec import MarkerSpec
from sldb.notations.notation_constants import (
    _ID,
    _NAME,
    ANY_RELATION,
    DEFAULT_NOTATIONS,
    DRAW_KINDS,
    KNOWN_RELATIONS,
    LAYOUT_KINDS,
    LEVELS,
    LINE_KINDS,
    NOTATIONS_DIR,
    SHAPES,
    TERMINALS,
)
from sldb.notations.notation_files import (
    builtin_notations,
    glyph_ref,
    link_ref,
    load_notation,
    notation_ref,
    resolve_notation,
)
from sldb.notations.notation_palette import notation_palette
from sldb.notations.notation_spec import NotationSpec
from sldb.notations.notation_style_check import check_notation_style
from sldb.notations.where_check import _check_where

__all__ = [
    "DEFAULT_NOTATIONS", "KNOWN_RELATIONS", "ANY_RELATION", "TERMINALS", "DRAW_KINDS", "LINE_KINDS", "LEVELS", "LAYOUT_KINDS", "SHAPES",
    "DiagramType", "NotationSpec", "GlyphSpec", "LinkSpec", "LinkEndSpec", "MarkerSpec",
    "builtin_notations", "resolve_notation", "load_notation", "check_notation_style", "notation_palette",
    "notation_ref", "glyph_ref", "link_ref",
]

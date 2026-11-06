"""Notations and projection views API for SLDB."""

from __future__ import annotations

from sldb.api.notations.notation_sync import (
    NotationSync,
    PaletteSync,
    SyncReport,
    sync_notation,
    sync_palette,
)
from sldb.api.notations.notation_view import (
    FRAGMENT_KINDS,
    ViewError,
    flatten,
    fragment_kind,
    fragments_of,
    link_order,
    lookup,
    matches,
    render_keyword,
    render_template,
    resolve_documents,
    resolve_view,
)
from sldb.api.notations.projection_view import (
    evaluate_projection_view,
    list_projection_views,
    node_id,
    save_projection_view,
)

__all__ = [
    "resolve_view",
    "resolve_documents",
    "evaluate_projection_view",
    "list_projection_views",
    "save_projection_view",
    "sync_notation",
    "sync_palette",
    "ViewError",
    "SyncReport",
    "PaletteSync",
    "NotationSync",
    "flatten",
    "lookup",
    "render_template",
    "render_keyword",
    "matches",
    "link_order",
    "fragments_of",
    "fragment_kind",
    "FRAGMENT_KINDS",
    "node_id",
]

# `sldb.notations` es vocabulario (capa 0) y no puede importar `sldb.api`: le conectamos el parser.
from sldb.api.where import where_matches as _where_matches
from sldb.notations.where_check import set_where_parser as _set_where_parser

_set_where_parser(lambda expression: _where_matches(expression, {}))

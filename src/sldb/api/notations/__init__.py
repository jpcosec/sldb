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
from sldb.api.notations.spec_models import load_spec, validate_spec
from sldb.api.notations.component_spec_constants import CONTAINS_RELATION, DEFAULT_EXCLUDED_RELATIONS, DEFAULT_NODE_TYPES
from sldb.api.notations.component_spec_graph import component_spec_from_graph
from sldb.api.notations.component_spec_ids import document_ref, node_kind, sanitize_id
from sldb.api.notations.component_spec_loaders import index_graph, load_node_link, load_node_link_graph
from sldb.api.notations.component_spec_python import component_spec_from_python
from sldb.api.notations.component_spec_python_build import write_component_spec
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
    "load_spec",
    "validate_spec",
    "component_spec_from_graph",
    "component_spec_from_python",
    "write_component_spec",
    "load_node_link",
    "load_node_link_graph",
    "index_graph",
    "node_kind",
    "document_ref",
    "sanitize_id",
    "DEFAULT_NODE_TYPES",
    "DEFAULT_EXCLUDED_RELATIONS",
    "CONTAINS_RELATION",
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
from sldb.notations.where_check import connect_where_check as _connect_where_check

_connect_where_check(lambda expression: _where_matches(expression, {}))

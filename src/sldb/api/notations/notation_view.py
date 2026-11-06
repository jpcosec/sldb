"""The single interpreter of the notation contract (`docs/architecture/notations-and-views.md`)."""

from __future__ import annotations

from sldb.api.notations.fragments import FRAGMENT_KINDS, fragment_kind, fragments_of
from sldb.api.notations.link_view import link_order
from sldb.api.notations.resolve_documents import resolve_documents
from sldb.api.notations.resolve_view import resolve_view
from sldb.api.notations.template_render import flatten, lookup, matches, render_keyword, render_template
from sldb.api.notations.view_error import ViewError

__all__ = [
    "resolve_view",
    "resolve_documents",
    "render_keyword",
    "ViewError",
    "flatten",
    "lookup",
    "render_template",
    "matches",
    "link_order",
    "fragments_of",
    "fragment_kind",
    "FRAGMENT_KINDS",
]

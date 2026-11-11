"""The composed views a store holds (GD25, q11), and the loading of one ViewDoc by name.

A ViewDoc is read from its own file through its model (the index's projection keeps no
nested `sections`); the `ViewDoc` nodes of the composed index (the store's and its linked
stores', H9) say which exist, `view_source` which one a name means and where its file is."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.api.views.view_source import VIEW_MODEL, bare_name, qualified_name, read_view_node, readable_view_node, view_node
from sldb.core.exceptions import SLDBValidationError
from sldb.models.notation.view_doc import ViewDoc


def list_views(store: str | Path | None) -> list[dict[str, Any]]:
    """`[{name, title, params, sections: [key...]}]` of the ViewDocs with sections, local and
    linked, by name; a linked view whose name another view also has is listed `<link>:<name>`.
    The projection views (no sections) are listed by `list_projection_views` (SV02)."""
    index = load_edge_index(open_store(store, mode="readonly").store_path, include_linked=True)
    nodes = index.nodes_of_type(VIEW_MODEL)
    clashes = Counter(n.semantics["export_id"] for n in nodes)
    named = [(listed_name(n, clashes), view) for n in nodes if (view := readable_view_node(n)) is not None]  # a refused path is warned, not listed
    return [summary(name, view) for name, view in sorted(named, key=lambda nv: nv[0]) if view.sections]


def listed_name(node: Any, clashes: Counter) -> str:
    """The view's bare name, or `<link>:<name>` for a linked view sharing its name."""
    return qualified_name(node) if clashes[node.semantics["export_id"]] > 1 else bare_name(node)


def summary(name: str, view: ViewDoc) -> dict[str, Any]:
    return {"name": name, "title": view.title, "params": [p.model_dump() for p in view.params], "sections": [s.key for s in view.sections]}


def load_view(name: str, index: Any) -> tuple[ViewDoc, Any]:
    """The composed ViewDoc `name` and its index node (`view_source.view_node`); unknown or
    ambiguous is `SLDBDocumentTargetError`, a projection view (no sections) is
    `SLDBValidationError`, both naming it."""
    node = view_node(index, name)
    view = read_view_node(node)
    if not view.sections:
        raise SLDBValidationError(f"view {name!r} is a projection view (it has no sections); use /views/projection")
    return view, node

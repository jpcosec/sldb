"""The composed views a store holds (GD25, q11), and the loading of one ViewDoc by name.

A ViewDoc is read from its own file through its model (the index's projection keeps no
nested `sections`); the `ViewDoc` nodes of the local index say which exist."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.models.notation.view_doc import ViewDoc
from sldb.runtime.validation import extract_model_data
from sldb.store.edge_index.node_ids import bare

VIEW_MODEL = "ViewDoc"


def list_views(store: str | Path | None) -> list[dict[str, Any]]:
    """`[{name, title, params, sections: [key...]}]` of the ViewDocs with sections, by name.
    The projection views (no sections) are listed by `list_projection_views` (SV02)."""
    store_path = open_store(store, mode="readonly").store_path
    index = load_edge_index(store_path, include_linked=False)
    views = [read_view(store_path, bare(node.id), index) for node in index.nodes_of_type(VIEW_MODEL)]
    return [summary(view) for view in sorted(views, key=lambda v: v.name) if view.sections]


def summary(view: ViewDoc) -> dict[str, Any]:
    return {"name": view.name, "title": view.title, "params": [p.model_dump() for p in view.params], "sections": [s.key for s in view.sections]}


def load_view(store_path: Path, name: str, index: Any) -> ViewDoc:
    """The composed ViewDoc `name`; unknown is `SLDBDocumentTargetError`, a projection view
    (no sections) is `SLDBValidationError`, both naming it."""
    view = read_view(store_path, f"{VIEW_MODEL}:{name}", index)
    if not view.sections:
        raise SLDBValidationError(f"view {name!r} is a projection view (it has no sections); use /views/projection")
    return view


def read_view(store_path: Path, export_id: str, index: Any) -> ViewDoc:
    """The ViewDoc `index` tracks as `export_id`, extracted from its file."""
    node = index.node(export_id)
    if node is None or node.node_type != VIEW_MODEL:
        raise SLDBDocumentTargetError(f"Unknown view: {export_id.split(':', 1)[-1]}")
    text = (open_store(store_path, mode="readonly").project_root / node.semantics["path"]).read_text(encoding="utf-8")
    return ViewDoc.model_validate(extract_model_data(ViewDoc, text))

"""Projection views: evaluate, list, and save ViewDoc projections in an SLDB store."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.projection_constants import DIRECTIONS, DOCUMENT_PREFIX, VIEW_MODEL, VIEWS_DIR, node_id
from sldb.api.notations.projection_edges import collect_edges
from sldb.api.notations.projection_filters import doc_title, is_selected, plan
from sldb.api.notations.projection_save import save_projection_view
from sldb.api.notations.projection_style import style_with_notation, view_layout
from sldb.api.notations.resolve_documents import resolve_documents
from sldb.api.notations.view_error import ViewError


def _view_of(view_or_ref: dict[str, Any] | str, documents: list[Any]) -> dict[str, Any]:
    """The view dict: given directly, or read from the `ViewDoc` it names."""
    if not isinstance(view_or_ref, str):
        return dict(view_or_ref)
    target_name = view_or_ref.split(":", 1)[-1]
    found = next((d for d in documents if d.model_name == VIEW_MODEL and d.name == target_name), None)
    if found is None:
        raise ViewError(f"ViewDoc '{view_or_ref}' is not in the store")
    return dict(found.payload or {})


def _result(view: dict[str, Any], selected: dict[str, Any], seen: set, documents: list[Any]) -> dict[str, Any]:
    """Nodes, edges and layout of the evaluated view."""
    return {
        "view": view,
        "nodes": [
            {"id": key, "model": d.model_name, "name": d.name, "title": doc_title(d), "payload": d.payload}
            for key, d in sorted(selected.items())
        ],
        "edges": [{"source": s, "target": t, "relation_type": r} for s, t, r in sorted(seen)],
        "layout": view_layout(view, documents),
    }


def evaluate_projection_view(
    store: Path | str,
    view_or_ref: dict[str, Any] | str,
    pythonpath: str | None = None,
) -> dict[str, Any]:
    """Evaluates a view (dict or ViewDoc ref) over `store`: `{view, nodes, edges, layout, [notation]}`."""
    store_path = Path(store)
    import sldb.api as api
    documents = api.load_runtime_documents(store_path, pythonpath, include_linked=False)
    view = _view_of(view_or_ref, documents)
    entries, relations, direction = plan(view)
    selected = {node_id(d.model_name, d.name): d for d in documents if is_selected(d, entries)}
    result = _result(view, selected, collect_edges(store_path, selected, relations, direction), documents)
    if view.get("notation"):
        result["notation"] = style_with_notation(store_path, view, result, documents, pythonpath)
    return result


def list_projection_views(
    store: Path | str,
    pythonpath: str | None = None,
) -> list[dict[str, Any]]:
    """List all `ViewDoc`s in the store as `[{ref, payload}]`."""
    store_path = Path(store)
    import sldb.api as api

    documents = api.load_runtime_documents(store_path, pythonpath, include_linked=False)
    return [
        {"ref": f"{VIEW_MODEL}:{d.name}", "payload": d.payload}
        for d in sorted(documents, key=lambda d: d.name)
        if d.model_name == VIEW_MODEL
    ]


__all__ = [
    "evaluate_projection_view",
    "list_projection_views",
    "save_projection_view",
    "ViewError",
    "node_id",
]

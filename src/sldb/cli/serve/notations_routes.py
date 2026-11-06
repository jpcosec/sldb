"""HTTP route handlers for notations and projection views in sldb serve."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path

from sldb.cli.serve.notations_payloads import (
    JsonDict,
    list_notations_payload,
    resolve_documents_payload,
    view_spec_payload,
)
from sldb.cli.serve.views_payloads import (
    evaluate_view_get_payload,
    evaluate_view_post_payload,
    list_views_payload,
    save_view_payload,
)

_NOTATION_ROUTES = {
    ("GET", "/notations"): list_notations_payload,
    ("GET", "/notations/view"): view_spec_payload,
    ("POST", "/notations/resolve"): resolve_documents_payload,
}

_VIEW_ROUTES = {
    ("GET", "/views/projection"): list_views_payload,
    ("GET", "/views/projection/evaluate"): evaluate_view_get_payload,
    ("POST", "/views/projection/evaluate"): evaluate_view_post_payload,
    ("POST", "/views/projection/save"): save_view_payload,
}


def _dispatch(routes: dict, handler: BaseHTTPRequestHandler, method: str, route: str, store_path: Path, pythonpath: str):
    """Run the payload builder registered for `(method, route)`, else a 404."""
    action = routes.get((method, route))
    if action is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return action(handler, store_path, pythonpath)


def dispatch_notations(
    handler: BaseHTTPRequestHandler,
    method: str,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    """Dispatch GET/POST /notations* routes."""
    return _dispatch(_NOTATION_ROUTES, handler, method, route, store_path, pythonpath)


def dispatch_projection_views(
    handler: BaseHTTPRequestHandler,
    method: str,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    """Dispatch GET/POST /views/projection* routes."""
    return _dispatch(_VIEW_ROUTES, handler, method, route, store_path, pythonpath)

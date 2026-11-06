"""Payload builders for the `/views/projection*` routes of sldb serve."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path

from sldb.api import evaluate_projection_view, list_projection_views, save_projection_view
from sldb.cli.serve.notations_payloads import JsonDict, attempt
from sldb.cli.serve.params import query_params
from sldb.cli.serve.responses import read_json_body


def list_views_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """The projection views in the store."""
    return {"ok": True, "views": list_projection_views(store_path, pythonpath)}, 200


def evaluate_view_get_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Evaluate the view named by the `view`, `ref` or `name` query parameter."""
    params = query_params(handler)
    view_ref = params.get("view") or params.get("ref") or params.get("name")
    if not view_ref:
        return {"ok": False, "error": "Missing parameter: view (or ref)"}, 400
    return attempt(lambda: evaluate_projection_view(store_path, view_ref, pythonpath=pythonpath))


def evaluate_view_post_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Evaluate the view (or ref) in the request body."""
    body = read_json_body(handler)
    view_or_ref = body.get("view") or body.get("ref") or body
    if not view_or_ref:
        return {"ok": False, "error": "Body must contain view definition or reference"}, 400
    return attempt(lambda: evaluate_projection_view(store_path, view_or_ref, pythonpath=pythonpath))


def save_view_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Save the view in the request body under `name`."""
    body = read_json_body(handler)
    name = body.get("name")
    view = body.get("view") or body
    if not name or not isinstance(view, dict):
        return {"ok": False, "error": "Body must contain 'name' and 'view' object"}, 400
    return attempt(lambda: save_projection_view(store_path, name, view, pythonpath=pythonpath))

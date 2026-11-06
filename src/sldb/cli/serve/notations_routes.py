"""HTTP route handlers for notations and projection views in sldb serve."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
)
from sldb.cli.serve.params import query_params, require_param
from sldb.cli.serve.responses import read_json_body
from sldb.notations.notation import builtin_notations
from sldb.notations.palette import builtin_palettes

JsonDict = dict[str, Any]


def dispatch_notations(
    handler: BaseHTTPRequestHandler,
    method: str,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    """Dispatch GET/POST /notations* routes."""
    if method == "GET":
        if route == "/notations":
            return list_notations_payload(handler, store_path, pythonpath)
        if route == "/notations/view":
            return view_spec_payload(handler, store_path, pythonpath)
    elif method == "POST":
        if route == "/notations/resolve":
            return resolve_documents_payload(handler, store_path, pythonpath)

    return {"ok": False, "error": f"Unknown route: {route}"}, 404


def dispatch_projection_views(
    handler: BaseHTTPRequestHandler,
    method: str,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    """Dispatch GET/POST /views/projection* routes."""
    if route == "/views/projection" and method == "GET":
        return list_views_payload(handler, store_path, pythonpath)
    if route == "/views/projection/evaluate":
        if method == "GET":
            return evaluate_view_get_payload(handler, store_path, pythonpath)
        if method == "POST":
            return evaluate_view_post_payload(handler, store_path, pythonpath)
    if route == "/views/projection/save" and method == "POST":
        return save_view_payload(handler, store_path, pythonpath)

    return {"ok": False, "error": f"Unknown route: {route}"}, 404


def list_notations_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    builtins = sorted(builtin_notations())
    palettes = sorted(builtin_palettes())
    store_notations: list[str] = []
    try:
        import sldb.api as api

        docs = api.load_runtime_documents(store_path, pythonpath, include_linked=False)
        store_notations = [f"NotationDoc:{d.name}" for d in docs if d.model_name == "NotationDoc"]
    except Exception:
        pass

    return {
        "ok": True,
        "builtin_notations": builtins,
        "builtin_palettes": palettes,
        "store_notations": store_notations,
    }, 200


def view_spec_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    spec, error = require_param(query_params(handler), "spec")
    if error is not None:
        return error, 400
    try:
        res = resolve_view(store_path, spec, pythonpath=pythonpath)
        return {"ok": True, **res}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400


def resolve_documents_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    body = read_json_body(handler)
    notation = body.get("notation")
    doc_refs = body.get("docs") or body.get("doc_refs")
    if not notation or not isinstance(doc_refs, list):
        return {"ok": False, "error": "Body must contain 'notation' and 'docs' (or 'doc_refs') list"}, 400

    relation_refs = body.get("relations") or body.get("relation_refs")
    spec_style = body.get("spec_style") or body.get("style")
    try:
        res = resolve_documents(
            store_path,
            notation,
            doc_refs,
            relation_refs=relation_refs,
            spec_style=spec_style,
            pythonpath=pythonpath,
        )
        return {"ok": True, **res}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400


def list_views_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    views = list_projection_views(store_path, pythonpath)
    return {"ok": True, "views": views}, 200


def evaluate_view_get_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    params = query_params(handler)
    view_ref = params.get("view") or params.get("ref") or params.get("name")
    if not view_ref:
        return {"ok": False, "error": "Missing parameter: view (or ref)"}, 400
    try:
        res = evaluate_projection_view(store_path, view_ref, pythonpath=pythonpath)
        return {"ok": True, **res}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400


def evaluate_view_post_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    body = read_json_body(handler)
    view_or_ref = body.get("view") or body.get("ref") or body
    if not view_or_ref:
        return {"ok": False, "error": "Body must contain view definition or reference"}, 400
    try:
        res = evaluate_projection_view(store_path, view_or_ref, pythonpath=pythonpath)
        return {"ok": True, **res}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400


def save_view_payload(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    body = read_json_body(handler)
    name = body.get("name")
    view = body.get("view") or body
    if not name or not isinstance(view, dict):
        return {"ok": False, "error": "Body must contain 'name' and 'view' object"}, 400
    try:
        res = save_projection_view(store_path, name, view, pythonpath=pythonpath)
        return {"ok": True, **res}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api import serialize_document  # re-export: data contract moved to sldb.api; kept for backwards compatibility
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.edges_routes import dispatch_edge
from sldb.cli.serve.document_routes import dispatch_document
from sldb.cli.serve.docs_routes import dispatch_docs
from sldb.cli.serve.graph_routes import dispatch_graph
from sldb.cli.serve.lint_routes import dispatch_lint
from sldb.cli.serve.models_routes import dispatch_models
from sldb.cli.serve.responses import read_json_body, send_json, send_common_headers
from sldb.cli.serve.save_routes import save_request
from sldb.cli.serve.schema import schema_models
from sldb.store.export import export_kgdb_semantic_payload
from sldb.store.query import load_runtime_documents


def dispatch(
    handler: BaseHTTPRequestHandler,
    method: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    if method == "GET":
        return dispatch_get(handler, route, store_path, project_root, pythonpath)
    if method == "POST":
        return dispatch_post(handler, route, store_path, project_root, pythonpath)
    return {"ok": False, "error": "Method not allowed"}, 405


def dispatch_get(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    handlers = {"/health": health_payload, "/schema": lambda *_: {"models": schema_models(store_path, pythonpath)}, "/graph": lambda *_: {"documents": graph_documents(store_path, pythonpath)}, "/kgdb/snapshot": lambda *_: export_kgdb_semantic_payload(store_path, project_root, resolve_model_ref, pythonpath)}
    if route in handlers:
        return handlers[route](route), 200
    return _nested_get(handler, route, store_path, project_root, pythonpath)


def _nested_get(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    if route == "/edges" or route.startswith("/edges/"):
        return dispatch_edge(handler, store_path)
    if route.startswith("/graph/"):
        return dispatch_graph(handler, store_path)
    if route == "/document" or route == "/document/ir":
        return dispatch_document(handler, route, store_path, project_root, pythonpath)
    if route == "/models" or route.startswith("/models/"): return dispatch_models(handler, "GET", route, store_path, project_root, pythonpath)
    if route == "/lint": return dispatch_lint(handler, store_path, project_root, pythonpath)
    return {"ok": False, "error": f"Unknown route: {route}"}, 404


def health_payload(_: str) -> dict[str, Any]:
    return {"status": "ok"}


def graph_documents(store_path: Path, pythonpath: str) -> list[dict[str, Any]]:
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    return [serialize_document(doc) for doc in docs]


def dispatch_post(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    if route.startswith("/models/"):
        return dispatch_models(handler, "POST", route, store_path, project_root, pythonpath)
    if route.startswith("/docs/"):
        return dispatch_docs(handler, route, store_path, project_root, pythonpath)
    if route != "/save":
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return save_request(read_json_body(handler), store_path, project_root, pythonpath)


def handle_options(handler: BaseHTTPRequestHandler, cors: bool) -> None:
    if not cors:
        send_json(handler, 404, {"ok": False, "error": "CORS disabled"}, cors)
        return
    handler.send_response(204)
    send_common_headers(handler, 0, cors)
    handler.end_headers()

"""GET /document*: one tracked document, its IR alone, or its segments.

The IR is built by the CLI's real builder, re-exported through ``sldb.api``
(``build_document_ir_json``); nothing here reimplements markdown parsing.
Doc inexistente -> 404; IR no construible (modelo no resoluble, roundtrip
roto) -> 422, sin reventar el endpoint. Las tres rutas comparten el chequeo
de existencia, así que el 404 es el mismo por la misma razón.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import build_document_ir_json
from sldb.cli.graph_ops import resolve_runtime_doc
from sldb.cli.serve.params import query_params, require_param
from sldb.cli.serve.segments_routes import segments_response
from sldb.cli.serve.tracked_docs import is_tracked

JsonDict = dict[str, Any]
DOCUMENT_ROUTES = ("/document", "/document/ir", "/document/segments")


def dispatch_document(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[JsonDict, int]:
    name, error = require_param(query_params(handler), "id")
    if error is not None:
        return error, 400
    if not is_tracked(store_path, project_root, name):
        return {"ok": False, "error": f"Unknown doc: {name}"}, 404
    return _respond(route, name, store_path, pythonpath)


def _respond(route: str, name: str, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    if route == "/document/segments":
        return segments_response(store_path, pythonpath, name)
    return _respond_ir(route, name, store_path, pythonpath)


def _respond_ir(route: str, name: str, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    try:
        runtime_doc = resolve_runtime_doc(str(store_path), name, pythonpath)
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 422
    ir = _ir_json(runtime_doc)
    if isinstance(ir, str):
        return {"ok": False, "error": ir}, 422
    if route == "/document/ir":
        return ir, 200
    return {**_flat(runtime_doc), "ir": ir}, 200


def _ir_json(runtime_doc: dict[str, Any]) -> JsonDict | str:
    try:
        markdown = Path(runtime_doc["absolute_path"]).read_text(encoding="utf-8")
        return build_document_ir_json(runtime_doc, markdown, runtime_doc.get("template"))
    except Exception as exc:
        return str(exc)


def _flat(runtime_doc: dict[str, Any]) -> JsonDict:
    return {
        "id": runtime_doc["name"],
        "model_name": runtime_doc["model"],
        "path": runtime_doc["path"],
        "payload": runtime_doc["payload"],
        "semantic_tags": runtime_doc["semantic_tags"],
    }
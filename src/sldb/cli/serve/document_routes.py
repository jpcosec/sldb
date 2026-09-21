"""GET /document*: one tracked document (with its full IR) or the IR alone.

The IR is built by the CLI's real builder, re-exported through ``sldb.api``
(``build_document_ir_json``); nothing here reimplements markdown parsing.
Doc inexistente -> 404; IR no construible (modelo no resoluble, roundtrip
roto) -> 422, sin reventar el endpoint.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import build_document_ir_json
from sldb.cli.graph_ops import resolve_runtime_doc
from sldb.cli.serve.params import query_params, require_param
from sldb.store.io import load_documents_index, load_models_index, load_store_index

JsonDict = dict[str, Any]


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
    if not _is_tracked(store_path, project_root, name):
        return {"ok": False, "error": f"Unknown doc: {name}"}, 404
    return _respond(route, name, store_path, pythonpath)


def _respond(route: str, name: str, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
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


def _is_tracked(store_path: Path, root: Path, name: str) -> bool:
    index = load_store_index(store_path)
    for model in index.models:
        m_idx = load_models_index(root / model.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        if any(doc.name == name for doc in d_idx.documents):
            return True
    return False


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
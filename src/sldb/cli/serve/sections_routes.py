"""GET /sections: one document's sections, straight from its DocumentIR.

The IR the CLI's real builder produces already carries the sections in
``context_index``; nothing here recomputes or re-parses markdown. Each section is
its path/title/breadcrumbs/semantic tags plus the ``field_path`` of every IR node
the section owns, so the editor can paint field chips per section.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import build_document_ir_json, runtime_document
from sldb.cli.serve.params import query_params, require_param


def dispatch_sections(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    doc, error = require_param(query_params(handler), "doc")
    if error is not None:
        return error, 400
    runtime, error = _find(store_path, pythonpath, doc)
    if error is not None:
        return error, 404
    ir, error = _ir_json(runtime, project_root)
    if error is not None:
        return error, 422
    return {"doc": runtime.name, "sections": [_section(entry, ir, runtime) for entry in ir["context_index"]]}, 200


def _find(store_path: Path, pythonpath: str, doc: str) -> tuple[Any, dict[str, Any] | None]:
    try:
        return runtime_document(store_path, pythonpath, doc), None
    except ValueError as exc:
        return None, {"ok": False, "error": str(exc)}


def _ir_json(runtime: Any, root: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    try:
        markdown = Path(root / runtime.path).read_text(encoding="utf-8")
        runtime_dict = {"store": runtime.store_name, "model": runtime.model_name, "name": runtime.name, "path": runtime.path, "payload": runtime.payload, "semantic_tags": runtime.semantic_tags}
        return build_document_ir_json(runtime_dict, markdown, getattr(runtime.model_type, "__template__", None)), None
    except Exception as exc:
        return {}, {"ok": False, "error": str(exc)}


def _section(entry: dict[str, Any], ir: dict[str, Any], runtime: Any) -> dict[str, Any]:
    owned = [node.get("field_path") for node in ir.get("nodes", []) if node.get("owning_section") == entry.get("path")]
    return {
        "doc": runtime.name,
        "path": entry.get("path"),
        "title": entry.get("title"),
        "breadcrumbs": entry.get("breadcrumbs") or [],
        "semantic_tags": entry.get("semantic_tags") or [],
        "about": entry.get("about") or [],
        "field_paths": [field for field in owned if field],
    }
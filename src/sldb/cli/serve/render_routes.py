"""GET /extract and GET /render: a document's data and its template rendering.

``/extract?doc=<id>&format=json|yaml`` returns only the extracted payload; the
yaml format embeds the payload as a YAML string (the transport stays JSON-only).
``/render?doc=<id>&format=md|html`` renders the document through its model with
the CLI's renderer — the same path AntonIA's wiki uses (`sldb render` ->
`render_model_markdown`). There is no in-repo markdown-to-HTML converter, so
``format=html`` returns the same markdown source and the client converts (the
wiki's contract: markdown feeds Astro). ``/render?model=<M>`` returns the model's
``__template__`` as sample text.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

import yaml

from sldb.api import extract_document_payload, render_document_markdown, render_model_template
from sldb.cli.serve.params import query_params, require_param


def dispatch_render(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    if route == "/extract":
        return _extract(params, store_path, pythonpath)
    model = params.get("model")
    if model is not None:
        return _model_sample(model, store_path, pythonpath)
    return _render_doc(params, store_path, pythonpath)


def _extract(params: dict[str, str], store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    doc, error = require_param(params, "doc")
    if error is not None:
        return error, 400
    try:
        payload = extract_document_payload(store_path, pythonpath, doc)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 404
    if params.get("format") == "yaml":
        return {"doc": doc, "payload": yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)}, 200
    return {"doc": doc, "payload": payload}, 200


def _render_doc(params: dict[str, str], store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    doc, error = require_param(params, "doc")
    if error is not None:
        return error, 400
    try:
        markdown = render_document_markdown(store_path, pythonpath, doc)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 404
    return {"doc": doc, "format": params.get("format", "md"), "markdown": markdown}, 200


def _model_sample(model: str, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    try:
        return {"model": model, "template": render_model_template(store_path, pythonpath, model)}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 404
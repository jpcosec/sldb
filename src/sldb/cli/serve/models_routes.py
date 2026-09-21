"""GET/POST /models*: model lifecycle over the native sldb API (no pron). Drafts per pron spec 12 §4."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import (add_model_field, describe_model, edit_model_template, promote_model_draft, remove_model_field, validate_model_draft)
from sldb.cli.serve.params import query_params, require_param
from sldb.cli.serve.responses import read_json_body
from sldb.core.exceptions import SLDBError
from sldb.store.io import load_documents_index, load_models_index, load_store_index

JsonDict = dict[str, Any]


def dispatch_models(handler, method, route, store_path, project_root, pythonpath):
    table = _GET_ROUTES if method == "GET" else _POST_ROUTES
    callback = table.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return callback(handler, store_path, project_root, pythonpath)


def catalog_payload(handler, store_path, project_root, pythonpath):
    return {"models": _catalog(store_path, project_root)}, 200


def _model_entry(entry, m_idx, d_idx):
    return {"name": entry.name, "model_ref": entry.model_ref, "path": entry.path, "version": m_idx.version, "canonical": getattr(m_idx, "canonical", False), "family": getattr(m_idx, "family", None), "semantics": list(getattr(m_idx, "semantics", [])), "documents": len(d_idx.documents)}


def _catalog(store_path, root):
    index = load_store_index(store_path)
    models = []
    for entry in sorted(index.models, key=lambda m: m.name):
        m_idx = load_models_index(root / entry.models_index)
        d_idx = load_documents_index(root / m_idx.documents_index)
        models.append(_model_entry(entry, m_idx, d_idx))
    return models


def detail_payload(handler, store_path, project_root, pythonpath):
    model, error = require_param(query_params(handler), "model")
    if error is not None:
        return error, 400
    return _describe(store_path, model, pythonpath)


def _describe(store_path, model, pythonpath):
    try:
        description = describe_model(store_path, model, pythonpath)
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, "model": description.model_dump(mode="json")}, 200


def fields_add_payload(handler, store_path, project_root, pythonpath):
    request, error = _require(handler, "model", "field_name")
    if error is not None:
        return error, 400
    return _run(store_path, pythonpath, lambda: add_model_field(store_path, request["model"], request["field_name"], request.get("field_type") or "str", str(request.get("description") or ""), request.get("default") or None, pythonpath), {"model": request["model"], "field_name": request["field_name"]})


def fields_remove_payload(handler, store_path, project_root, pythonpath):
    request, error = _require(handler, "model", "field_name")
    if error is not None:
        return error, 400
    return _run(store_path, pythonpath, lambda: remove_model_field(store_path, request["model"], request["field_name"], pythonpath), {"model": request["model"], "field_name": request["field_name"]})


def template_edit_payload(handler, store_path, project_root, pythonpath):
    request, error = _require(handler, "model", "content")
    if error is not None:
        return error, 400
    return _run(store_path, pythonpath, lambda: edit_model_template(store_path, request["model"], request["content"], pythonpath), {"model": request["model"]})


def validate_payload(handler, store_path, project_root, pythonpath):
    request, error = _require(handler, "model")
    if error is not None:
        return error, 400
    return _report(store_path, pythonpath, lambda: validate_model_draft(store_path, request["model"], pythonpath))


def promote_payload(handler, store_path, project_root, pythonpath):
    request, error = _require(handler, "model")
    if error is not None:
        return error, 400
    return _report(store_path, pythonpath, lambda: promote_model_draft(store_path, request["model"], pythonpath))


def _require(handler, *required):
    request = read_json_body(handler)
    for name in required:
        if not request.get(name):
            return None, {"ok": False, "error": f"Missing parameter: {name}"}
    return request, None


def _run(store_path, pythonpath, op, extra):
    try:
        draft = op()
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, "draft_path": str(draft.draft_path), **extra}, 200


def _report(store_path, pythonpath, op):
    try:
        report = op()
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, **report.model_dump(mode="json")}, 200


_GET_ROUTES = {"/models": catalog_payload, "/models/detail": detail_payload}
_POST_ROUTES = {"/models/fields-add": fields_add_payload, "/models/fields-remove": fields_remove_payload, "/models/template-edit": template_edit_payload, "/models/validate": validate_payload, "/models/promote": promote_payload}
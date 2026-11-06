"""GET/POST /models*: model lifecycle over the native sldb API (no pron). Drafts per pron spec 12 §4."""

from __future__ import annotations

from typing import Any

from sldb.api import describe_model
from sldb.cli.serve.models_create_routes import create_payload, metadata_edit_payload
from sldb.cli.serve.models_write_routes import fields_add_payload, fields_remove_payload, promote_payload, template_edit_payload, validate_payload
from sldb.cli.serve.params import query_params, require_param
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


_GET_ROUTES = {"/models": catalog_payload, "/models/detail": detail_payload}
_POST_ROUTES = {
    "/models/create": create_payload,
    "/models/fields-add": fields_add_payload,
    "/models/fields-remove": fields_remove_payload,
    "/models/metadata-edit": metadata_edit_payload,
    "/models/template-edit": template_edit_payload,
    "/models/validate": validate_payload,
    "/models/promote": promote_payload,
}
"""POST /models/create and /models/metadata-edit: the handlers that take class metadata."""

from __future__ import annotations

from sldb.api import create_model, edit_model_metadata
from sldb.cli.serve.models_route_support import require_fields, run_draft_op
from sldb.core.exceptions import SLDBError

_META_KEYS = ("containment", "references", "compositions", "semantics", "authority")


def create_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "name", "fields")
    if error is not None:
        return error, 400
    extras = {key: request.get(key) for key in _META_KEYS}
    try:
        reg = create_model(store_path, request["name"], request["fields"], template=request.get("template"), base=request.get("base"), target_package=request.get("target_package", "sldb_generated"), pythonpath=pythonpath or str(project_root), **extras)
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, **reg.model_dump(mode="json")}, 200


def metadata_edit_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model")
    if error is not None:
        return error, 400
    extras = {key: request.get(key) for key in _META_KEYS}
    return run_draft_op(store_path, pythonpath, lambda: edit_model_metadata(store_path, request["model"], pythonpath=pythonpath, **extras), {"model": request["model"]})

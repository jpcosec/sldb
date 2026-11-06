"""POST /models* handlers over fields, template, validation and promotion of a draft."""

from __future__ import annotations

from sldb.api import add_model_field, edit_model_template, promote_model_draft, remove_model_field, validate_model_draft
from sldb.cli.serve.models_route_support import require_fields, run_draft_op, run_report_op


def fields_add_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model", "field_name")
    if error is not None:
        return error, 400
    return run_draft_op(store_path, pythonpath, lambda: add_model_field(store_path, request["model"], request["field_name"], request.get("field_type") or "str", str(request.get("description") or ""), request.get("default") or None, pythonpath), {"model": request["model"], "field_name": request["field_name"]})


def fields_remove_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model", "field_name")
    if error is not None:
        return error, 400
    return run_draft_op(store_path, pythonpath, lambda: remove_model_field(store_path, request["model"], request["field_name"], pythonpath), {"model": request["model"], "field_name": request["field_name"]})


def template_edit_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model", "content")
    if error is not None:
        return error, 400
    return run_draft_op(store_path, pythonpath, lambda: edit_model_template(store_path, request["model"], request["content"], pythonpath), {"model": request["model"]})


def validate_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model")
    if error is not None:
        return error, 400
    return run_report_op(store_path, pythonpath, lambda: validate_model_draft(store_path, request["model"], pythonpath))


def promote_payload(handler, store_path, project_root, pythonpath):
    request, error = require_fields(handler, "model")
    if error is not None:
        return error, 400
    backfill = bool(request.get("backfill", False))
    return run_report_op(store_path, pythonpath, lambda: promote_model_draft(store_path, request["model"], pythonpath, backfill=backfill))

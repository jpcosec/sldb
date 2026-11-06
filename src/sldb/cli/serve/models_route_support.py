"""Shared pieces of the POST /models* handlers: required parameters and response shapes."""

from __future__ import annotations

from sldb.cli.serve.responses import read_json_body
from sldb.core.exceptions import SLDBError





def require_fields(handler, *required):
    request = read_json_body(handler)
    for name in required:
        if not request.get(name):
            return None, {"ok": False, "error": f"Missing parameter: {name}"}
    return request, None


def run_draft_op(store_path, pythonpath, op, extra):
    try:
        draft = op()
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, "draft_path": str(draft.draft_path), **extra}, 200


def run_report_op(store_path, pythonpath, op):
    try:
        report = op()
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 200
    return {"ok": True, **report.model_dump(mode="json")}, 200

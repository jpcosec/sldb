"""GET /edges/referrers?target= and POST /edges/rewrite {target, replacement, dry_run}: the
`sldb edges referrers` list and the `sldb edges rewrite` report over HTTP, same bodies as the
commands print with `--format json` (GD22).

`replacement` is required in the body: `null` removes the references, a string names what
they point at next; `dry_run` (optional, boolean, default false) reports without writing. A
missing or invalid parameter is 400; an unknown target is 404 and an ambiguous one 409, as in
`/docs/select`; a payload the model refuses, or a rule, is 400 with nothing written.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api.edges.referrers import referrers
from sldb.api.edges.rewrite_references import rewrite_references
from sldb.cli.serve.params import query_params, require_param
from sldb.cli.serve.responses import read_json_body
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBError

Response = tuple[Any, int]


def dispatch_edges_rewrite(handler: BaseHTTPRequestHandler, method: str, store_path: Path, pythonpath: str | None) -> Response:
    """`/edges/referrers` on GET, `/edges/rewrite` on POST."""
    try:
        if method == "GET":
            return referrers_route(query_params(handler), store_path, pythonpath)
        return rewrite_route(read_json_body(handler), store_path, pythonpath)
    except (SLDBError, ValueError) as exc:
        return _refused(exc)


def referrers_route(params: dict[str, str], store_path: Path, pythonpath: str | None) -> Response:
    target, error = require_param(params, "target")
    if error is not None:
        return error, 400
    return [referrer.to_dict() for referrer in referrers(store_path, target, pythonpath)], 200


def rewrite_route(body: dict[str, Any], store_path: Path, pythonpath: str | None) -> Response:
    problem = _body_problem(body)
    if problem is not None:
        return {"ok": False, "error": problem}, 400
    return rewrite_references(store_path, body["target"], body["replacement"], dry_run=bool(body.get("dry_run", False)), pythonpath=pythonpath).to_dict(), 200


def _body_problem(body: dict[str, Any]) -> str | None:
    if not isinstance(body.get("target"), str) or not body["target"]:
        return "Missing parameter: target"
    if "replacement" not in body:
        return "Missing parameter: replacement (a string, or null to remove the references)"
    if body["replacement"] is not None and not isinstance(body["replacement"], str):
        return "Invalid parameter replacement: expected a string or null"
    if not isinstance(body.get("dry_run", False), bool):
        return "Invalid parameter dry_run: expected true or false"
    return None


def _refused(exc: Exception) -> Response:
    """404 unknown target, 409 ambiguous, 400 for anything else refused."""
    if isinstance(exc, SLDBDocumentTargetError):
        return {"ok": False, "error": str(exc)}, 409 if "Ambiguous" in str(exc) else 404
    return {"ok": False, "error": str(exc)}, 400

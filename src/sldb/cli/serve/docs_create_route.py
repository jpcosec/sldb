"""POST /docs: create and track one document; the compact face of POST /docs/create."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.cli.serve.docs_routes import create_action, dispatch_docs
from sldb.cli.serve.responses import read_json_body
from sldb.cli.serve.save_plan import bad
from sldb.cli.serve.save_routes import SAVE_LOCK

_KEYS = ("model", "name", "payload")


def dispatch_docs_or_create(handler: Any, route: str, store_path: Path, project_root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """`POST /docs` is the compact create; `/docs/create|track|untrack` keep their contract."""
    if route == "/docs":
        return create_doc_response(handler, store_path, project_root, pythonpath)
    return dispatch_docs(handler, route, store_path, project_root, pythonpath)


def create_doc_response(handler: Any, store_path: Path, project_root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """Create `{model, name, payload}` under the same lock /save uses.

    Returns `{ok, id, version}` (200), or `{ok: false, error}` with 400 (malformed body
    or name), 404 (model not registered), 409 (name taken) or 422 (invalid payload).
    """
    try:
        request = read_json_body(handler)
    except ValueError:
        return bad("Body inválido: se esperaba un objeto JSON.")
    if not _well_formed(request):
        return bad("Body inválido: se esperaba {model, name, payload} con payload objeto.")
    with SAVE_LOCK:
        body, status = create_action({key: request[key] for key in _KEYS}, store_path, project_root, pythonpath)
    return (_created(body), status) if status == 200 else (body, status)


def _well_formed(request: dict[str, Any]) -> bool:
    return all(isinstance(request.get(key), str) for key in ("model", "name")) and isinstance(request.get("payload"), dict)


def _created(body: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "id": body["doc"]["id"], "version": body["doc"]["version"]}

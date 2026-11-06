"""Payload builders for the `/notations*` routes of sldb serve."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Callable

from sldb.api import resolve_documents, resolve_view
from sldb.api.notations.notation_listing import list_notations
from sldb.cli.serve.params import query_params, require_param
from sldb.cli.serve.responses import read_json_body

JsonDict = dict[str, Any]


def attempt(call: Callable[[], JsonDict]) -> tuple[JsonDict, int]:
    """`({"ok": True, **call()}, 200)`, or a 400 error payload if the call raises."""
    try:
        return {"ok": True, **call()}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 400


def list_notations_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Builtin notations and palettes plus the notations in the store."""
    return {"ok": True, **list_notations(store_path, pythonpath)}, 200


def view_spec_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """The resolved view of the `spec` query parameter."""
    spec, error = require_param(query_params(handler), "spec")
    if error is not None:
        return error, 400
    return attempt(lambda: resolve_view(store_path, spec, pythonpath=pythonpath))


def _resolve(store_path: Path, notation: str, doc_refs: list, body: JsonDict, pythonpath: str) -> tuple[JsonDict, int]:
    """Resolve the documents of the request body under the notation."""
    relation_refs = body.get("relations") or body.get("relation_refs")
    spec_style = body.get("spec_style") or body.get("style")
    return attempt(lambda: resolve_documents(
        store_path, notation, doc_refs, relation_refs=relation_refs, spec_style=spec_style, pythonpath=pythonpath
    ))


def resolve_documents_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[JsonDict, int]:
    """Documents of the request body styled with a notation."""
    body = read_json_body(handler)
    notation = body.get("notation")
    doc_refs = body.get("docs") or body.get("doc_refs")
    if not notation or not isinstance(doc_refs, list):
        return {"ok": False, "error": "Body must contain 'notation' and 'docs' (or 'doc_refs') list"}, 400
    return _resolve(store_path, notation, doc_refs, body, pythonpath)

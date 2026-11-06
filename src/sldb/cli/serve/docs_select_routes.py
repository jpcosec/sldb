"""GET /docs/select: `sldb docs select` over HTTP, same parameters and same payload.

Query mapping: ref, prefix, path_glob, model, where (the selector's keys, as strings),
include_linked and one (flags: 1/true/yes/on). 404 when `one` finds nothing, 409 with
`candidates` when it finds several, 400 for a blank key, an unparseable `where` or a bad flag.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sldb.api.documents.select_documents import select_documents
from sldb.cli.commands.docs_select import selection_payload, selector_of
from sldb.cli.serve.params import query_params
from sldb.core.exceptions import AmbiguousSelectionError, SLDBDocumentTargetError

_TRUE = {"1", "true", "yes", "on"}


def dispatch_docs_select(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    selector = selector_of({**params, "include_linked": _flag(params, "include_linked")})
    expect = "one" if _flag(params, "one") else "many"
    try:
        return selection_payload(selector, expect, select_documents(store_path, selector, expect=expect)), 200
    except (ValidationError, ValueError) as exc:
        return _refused(exc)


def _refused(exc: Exception) -> tuple[dict[str, Any], int]:
    """404 unknown, 409 ambiguous (with its candidates), 400 for anything the selector rejects."""
    if isinstance(exc, AmbiguousSelectionError):
        return {"ok": False, "error": str(exc), "candidates": exc.candidates}, 409
    if isinstance(exc, SLDBDocumentTargetError):
        return {"ok": False, "error": str(exc)}, 404
    return {"ok": False, "error": str(exc)}, 400


def _flag(params: dict[str, str], name: str) -> bool:
    return params.get(name, "0").lower() in _TRUE

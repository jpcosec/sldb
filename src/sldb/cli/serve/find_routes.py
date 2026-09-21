"""GET /find: the CLI's `sldb find` as JSON, served through sldb.api.

Query mapping: q=term, in=physical|semantic (all -> both, the CLI's default),
type=all|store|model|doc|section|field, where=<predicate>, select=<comma
fields>, limit=<n>; the flags regex, fuzzy and global (linked stores) mirror
the CLI's --regex/--fuzzy/--global. Omitted by design: --store and --pythonpath
are fixed by the server, --format is JSON by construction, and --rebuild is a
section-index mutation, not a query concern, so the HTTP surface never mutates.
An unparseable --where returns 400 with the parse engine's real message
(WherePredicateError, raised before any matching); malformed parameters are
also 400.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api import search
from sldb.cli.serve.params import query_params, require_param
from sldb.core.exceptions import SLDBError

_SEARCH_IN = {"physical", "semantic", "both", "all"}
_TYPES = {"all", "store", "model", "doc", "section", "field"}


def dispatch_find(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    plan, error = _parse(query_params(handler))
    if error is not None:
        return error, 400
    try:
        return search(store_path, pythonpath=pythonpath, **plan), 200
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 400


def _parse(params: dict[str, str]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    term, error = require_param(params, "q")
    search_in, e2 = _search_in(params.get("in"))
    kinds, e3 = _kinds(params.get("type"))
    limit, e4 = _limit(params.get("limit"))
    error = error or e2 or e3 or e4
    if error is not None:
        return {}, error
    return {"term": term, "search_in": search_in, "kinds": kinds, "where": params.get("where"), "select": params.get("select"), "limit": limit, "regex": _flag(params, "regex"), "fuzzy": _flag(params, "fuzzy"), "include_linked": _flag(params, "global")}, None


def _search_in(raw: str | None) -> tuple[str | None, dict[str, Any] | None]:
    if raw in (None, "all", "both"):
        return "both", None
    if raw not in _SEARCH_IN:
        return None, {"ok": False, "error": "Invalid parameter in: expected one of all, physical, semantic"}
    return raw, None


def _kinds(raw: str | None) -> tuple[set[str] | None, dict[str, Any] | None]:
    if raw in (None, "all"):
        return None, None
    if raw not in _TYPES:
        return None, {"ok": False, "error": "Invalid parameter type: expected one of all, doc, field, model, section, store"}
    return {raw}, None


def _limit(raw: str | None) -> tuple[int | None, dict[str, Any] | None]:
    if raw is None:
        return None, None
    if not raw.isdigit() or int(raw) < 1:
        return None, {"ok": False, "error": "Invalid parameter limit: expected a positive integer"}
    return int(raw), None


def _flag(params: dict[str, str], name: str) -> bool:
    return params.get(name, "0").lower() in {"1", "true", "yes", "on"}
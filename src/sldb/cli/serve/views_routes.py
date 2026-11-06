"""GET /views and GET /views/<name>: the composed views (GD25) over HTTP.

`GET /views` answers `{"views": [...]}` as `sldb views list --format json` does. `GET
/views/<name>?k=v` answers exactly `sldb views run <name> --param k=v --format json`, with
`ETag` = its `revision`; a request whose `If-None-Match` carries that tag gets 304 and no
body. 404 for an unknown view, 400 for a projection view (no sections; `/views/projection*`
serves those, untouched) or a param the view rejects.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api.views import list_views, run_view
from sldb.cli.serve.params import query_params
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError


def dispatch_views(handler: BaseHTTPRequestHandler, route: str, store_path: Path) -> tuple:
    """`(payload, status)` or `(payload, status, headers)` for a `/views*` GET."""
    if route == "/views":
        return {"views": list_views(store_path)}, 200
    name = route.removeprefix("/views/")
    if not name or "/" in name:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    try:
        result = run_view(store_path, name, query_params(handler))
    except (SLDBDocumentTargetError, SLDBValidationError) as exc:
        return {"ok": False, "error": str(exc)}, (404 if isinstance(exc, SLDBDocumentTargetError) else 400)
    return conditional(handler, result)


def conditional(handler: BaseHTTPRequestHandler, result: dict[str, Any]) -> tuple:
    """The result with its `ETag`, or 304 when the request already holds that revision."""
    etag = f'"{result["revision"]}"'
    tags = given_tags(handler.headers.get("If-None-Match", ""))
    if "*" in tags or etag in tags:
        return {}, 304, {"ETag": etag}
    return result, 200, {"ETag": etag}


def given_tags(header: str) -> list[str]:
    """The entity tags an `If-None-Match` names (a weak one reads as strong; `*` is kept)."""
    return [tag.strip().removeprefix("W/") for tag in header.split(",") if tag.strip()]

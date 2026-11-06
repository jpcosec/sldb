"""GET /project-graph/* : `sldb graph project nodes|edges|missing` over HTTP, same payload.

`/project-graph/nodes?kind=`, `/project-graph/edges?from=|to=` (exactly one of them) and
`/project-graph/missing` answer the JSON the command prints with `--format json`. A missing or
contradictory parameter, and a store whose `store.yaml` declares no (or a bad) `project_graph`,
are 400 with `{"ok": false, "error": ...}`.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from sldb.api.edges.project_graph.store_project_graph import project_graph
from sldb.cli.commands.graph_project import edges_payload, missing_payload, nodes_payload
from sldb.cli.serve.params import query_params
from sldb.core.exceptions import SLDBStoreError

Route = Callable[[Path, dict[str, str]], tuple[dict[str, Any], int]]


def dispatch_project_graph(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    callback = PROJECT_GRAPH_ROUTES.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    try:
        return callback(store_path, query_params(handler))
    except (SLDBStoreError, ValueError, FileNotFoundError) as exc:
        return {"ok": False, "error": str(exc)}, 400


def nodes_route(store_path: Path, params: dict[str, str]) -> tuple[dict[str, Any], int]:
    return nodes_payload(project_graph(store_path), params.get("kind") or None), 200


def edges_route(store_path: Path, params: dict[str, str]) -> tuple[dict[str, Any], int]:
    from_id, to_id = params.get("from") or None, params.get("to") or None
    if (from_id is None) == (to_id is None):
        return {"ok": False, "error": "Expected exactly one parameter of 'from' and 'to'"}, 400
    return edges_payload(project_graph(store_path), from_id, to_id), 200


def missing_route(store_path: Path, params: dict[str, str]) -> tuple[dict[str, Any], int]:
    return missing_payload(project_graph(store_path)), 200


PROJECT_GRAPH_ROUTES: dict[str, Route] = {
    "/project-graph/nodes": nodes_route,
    "/project-graph/edges": edges_route,
    "/project-graph/missing": missing_route,
}

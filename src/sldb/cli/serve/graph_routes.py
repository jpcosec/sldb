"""GET /graph/* routes: whole-graph analysis over the real graph API."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api.graph.analyze import (
    graph_central,
    graph_components,
    graph_cycles,
    graph_isolated,
    graph_path,
)
from sldb.api.graph.neighborhood import collect_neighborhood
from sldb.cli.serve.params import optional_int, query_params, require_param, require_params


def dispatch_graph(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    callback = GRAPH_ROUTES.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return callback(handler, store_path)


def neighborhood_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    node, error = require_param(params, "node")
    if error is not None:
        return error, 400
    depth, error = optional_int(params, "depth", 1)
    if error is not None:
        return error, 400
    nodes = collect_neighborhood(store_path, [node], depth)
    return {"nodes": sorted(nodes)}, 200


def path_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    values, error = require_params(params, "source", "target")
    if error is not None:
        return error, 400
    found = graph_path(store_path, values[0], values[1])
    if found is None:
        return {"ok": False, "error": f"No path from {values[0]} to {values[1]}."}, 404
    return {"path": found}, 200


def cycles_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    limit, error = optional_int(query_params(handler), "limit", 10)
    if error is not None:
        return error, 400
    return {"cycles": graph_cycles(store_path, limit=limit)}, 200


def components_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    return {"components": graph_components(store_path)}, 200


def central_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    limit, error = optional_int(query_params(handler), "limit", 20)
    if error is not None:
        return error, 400
    ranked = graph_central(store_path, limit=limit)
    return {"central": [{"node": node, "score": score} for node, score in ranked]}, 200


def isolated_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    return {"isolated": graph_isolated(store_path)}, 200


GRAPH_ROUTES = {
    "/graph/neighborhood": neighborhood_payload,
    "/graph/path": path_payload,
    "/graph/cycles": cycles_payload,
    "/graph/components": components_payload,
    "/graph/central": central_payload,
    "/graph/isolated": isolated_payload,
}
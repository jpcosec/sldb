"""GET /edges* routes: read-only views over the real edge index API."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_records
from sldb.cli.serve.params import query_params, require_param


def dispatch_edge(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    callback = EDGE_ROUTES.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return callback(handler, store_path)


def edge_list_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    origin = params.get("from") or None
    target = params.get("to") or None
    relation = params.get("relation") or None
    if origin is not None:
        return edge_list(store_path, edges_from, origin, relation)
    if target is not None:
        return edge_list(store_path, edges_to, target, relation)
    return {"ok": False, "error": "Missing parameter: expected 'from' or 'to'"}, 400


def edge_list(store_path: Path, reader: Any, export_id: str, relation: str | None) -> tuple[dict[str, Any], int]:
    records = reader(store_path, export_id, relation)
    return {"edges": serialize_edge_records(records)}, 200


def node_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    node_id, error = require_param(query_params(handler), "id")
    if error is not None:
        return error, 400
    record = edge_node(store_path, node_id)
    if record is None:
        return {"ok": False, "error": f"Unknown node: {node_id}"}, 404
    return {"node": serialize_edge_node_record(record)}, 200


def nodes_of_type_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    node_type, error = require_param(query_params(handler), "type")
    if error is not None:
        return error, 400
    records = edge_nodes_of_type(store_path, node_type)
    return {"nodes": serialize_edge_node_records(records)}, 200


EDGE_ROUTES = {
    "/edges": edge_list_payload,
    "/edges/node": node_payload,
    "/edges/nodes": nodes_of_type_payload,
}
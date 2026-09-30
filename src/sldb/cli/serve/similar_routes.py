"""GET /similar: which nodes share the most targets with one node (`sldb.api.graph_similar`)."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph.analyze import graph_similar
from sldb.cli.serve.params import optional_int, query_params, require_param


def similar_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    """Serve `?id=&relations=&limit=&types=`.

    `id` is a node id (`sldb://document/Model:name`) or an export id (`Model:name`); `relations`
    defaults to `tagged_as`, `types` filters the answer by node class (e.g. `NoteDoc`).
    Returns `{"similar": [[node_id, shared_targets], ...]}` (most shared first, ties by id,
    exactly what `similar_to` returns) and 200; 400 without `id` or with a bad `limit`;
    404 when the store has no such node. An empty list means "nothing resembles it".
    """
    params = query_params(handler)
    node, error = require_param(params, "id")
    limit, limit_error = optional_int(params, "limit", 10)
    if error or limit_error:
        return error or limit_error, 400
    record = load_edge_index(store_path, True, ()).node(node)
    if record is None:
        return {"ok": False, "error": f"Unknown node: {node}"}, 404
    ranked = graph_similar(store_path, record.id, _csv(params, "relations") or ("tagged_as",), limit, _csv(params, "types"))
    return {"similar": [[found, shared] for found, shared in ranked]}, 200


def _csv(params: dict[str, str], name: str) -> list[str] | None:
    return [item for item in params.get(name, "").split(",") if item.strip()] or None

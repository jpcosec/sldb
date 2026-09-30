"""GET /edges without from/to: every document-to-document edge, for graph views."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from sldb.api.edges.document_edges import document_edges
from sldb.cli.serve.edges_routes import dispatch_edge
from sldb.cli.serve.params import query_params


def dispatch_edges(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """Serve `/edges` bare or with `id` as the document view; `from`/`to`/`/edges/*` as before."""
    if urlparse(handler.path).path == "/edges" and wants_document_edges(handler):
        return document_edges_payload(handler, store_path, pythonpath)
    return dispatch_edge(handler, store_path)


def wants_document_edges(handler: BaseHTTPRequestHandler) -> bool:
    """True when the query names neither `from` nor `to`, even blank (those keep the raw edge reader)."""
    named = parse_qs(urlparse(handler.path).query, keep_blank_values=True)
    return "from" not in named and "to" not in named


def document_edges_payload(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """`{edges: [{id, source, target, type, origin, relationDoc}]}`, optionally for `?id=Model:name`."""
    edges = document_edges(store_path, pythonpath, query_params(handler).get("id") or None)
    return {"edges": [edge.model_dump(by_alias=True) for edge in edges]}, 200

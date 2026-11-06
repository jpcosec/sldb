from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from typing import Any


JsonDict = dict[str, Any]


def handle_cors_headers(handler: BaseHTTPRequestHandler) -> None:
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")


def send_json(
    handler: BaseHTTPRequestHandler,
    status: int,
    payload: JsonDict,
    cors: bool,
    headers: dict[str, str] | None = None,
) -> None:
    """The payload as JSON with the common headers plus `headers` (an `ETag`, say); a 304 Not
    Modified carries the headers and no body."""
    data = b"" if status == 304 else json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    send_common_headers(handler, len(data), cors)
    for name, value in (headers or {}).items():
        handler.send_header(name, value)
    handler.end_headers()
    handler.wfile.write(data)


def send_common_headers(
    handler: BaseHTTPRequestHandler,
    length: int,
    cors: bool,
) -> None:
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(length))
    if cors:
        handle_cors_headers(handler)


def read_json_body(handler: BaseHTTPRequestHandler) -> JsonDict:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length) if length else b"{}"
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object")
    return data

"""Query-string parsing helpers for the serve routes."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from typing import Any
from urllib.parse import parse_qs, urlparse

JsonDict = dict[str, Any]


def query_params(handler: BaseHTTPRequestHandler) -> dict[str, str]:
    query = urlparse(handler.path).query
    return {key: values[0] for key, values in parse_qs(query).items()}


def require_param(params: dict[str, str], name: str) -> tuple[str, JsonDict | None]:
    value = params.get(name)
    if not value:
        return name, {"ok": False, "error": f"Missing parameter: {name}"}
    return value, None


def require_params(params: dict[str, str], *names: str) -> tuple[list[str], JsonDict | None]:
    values = []
    for name in names:
        value = params.get(name)
        if not value:
            return [], {"ok": False, "error": f"Missing parameter: {name}"}
        values.append(value)
    return values, None


def optional_int(params: dict[str, str], name: str, default: int) -> tuple[int, JsonDict | None]:
    raw = params.get(name)
    if raw is None:
        return default, None
    try:
        value = int(raw)
    except ValueError:
        return default, {"ok": False, "error": f"Invalid parameter {name}: expected an integer"}
    if value < 1:
        return default, {"ok": False, "error": f"Invalid parameter {name}: expected a positive integer"}
    return value, None
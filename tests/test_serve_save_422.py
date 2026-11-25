from __future__ import annotations

import json
from pathlib import Path

from tests.test_serve import _build_store, _request_json, _serve, _stop


def test_save_422_returns_pydantic_errors_as_details(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "bad", "action": "create", "model": "SimpleBook", "payload": {"title": 123}},
        ]}, expected_error=422)
        assert status == 422
        assert body["ok"] is False
        assert "validation error" in body["error"]
        details = body["details"]
        assert isinstance(details, list) and details
        assert all({"loc", "msg", "type"} <= set(item) for item in details)
        assert any("title" in item["loc"] for item in details)
        json.dumps(details)
    finally:
        _stop(server, thread)

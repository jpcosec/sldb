"""Auth mode of `sldb serve`: off by default, bearer token when configured.

Every case drives a REAL store (the same CLI helpers `tests/test_serve.py` uses)
behind a real `ThreadingHTTPServer` on an ephemeral port — no mocks.
"""

from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from sldb.cli.serve.http_server import build_handler
from tests.store.test_cli_store import _PY_ARGS, _doc_track, _init, _model_add

TOKEN = "s3cret-token"
NO_AUTH = {"ok": False, "error": "unauthorized"}


def _build_store(tmp_path: Path) -> Path:
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    return tmp_path / ".sldb"


def _serve(store: Path, token: str | None) -> tuple[ThreadingHTTPServer, str]:
    handler = build_handler(str(store), _PY_ARGS[1], cors=True, token=token)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def _call(url: str, *, method: str = "GET", token: str | None = None, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(url, method=method, data=data)
    if payload is not None:
        request.add_header("Content-Type", "application/json")
    if token is not None:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(request, timeout=5) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def test_serve_without_token_stays_open(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, base_url = _serve(store, token=None)
    try:
        assert _call(f"{base_url}/health") == (200, {"status": "ok"})
        assert _call(f"{base_url}/stores")[0] == 200
        assert _call(f"{base_url}/save", method="POST", payload={"doc": "book", "payload": {"title": "Open"}})[0] == 200
    finally:
        server.shutdown()
        server.server_close()


def test_serve_with_token_requires_the_bearer_token(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, base_url = _serve(store, token=TOKEN)
    try:
        assert _call(f"{base_url}/health") == (401, NO_AUTH)
        assert _call(f"{base_url}/health", token="wrong") == (401, NO_AUTH)
        assert _call(f"{base_url}/health", token=TOKEN) == (200, {"status": "ok"})
        assert _call(f"{base_url}/stores", token=TOKEN)[0] == 200
    finally:
        server.shutdown()
        server.server_close()


def test_serve_token_blocks_writes_and_leaves_the_store_untouched(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, base_url = _serve(store, token=TOKEN)
    try:
        status, body = _call(f"{base_url}/save", method="POST", payload={"doc": "book", "payload": {"title": "Hacked"}})
        assert (status, body) == (401, NO_AUTH)

        _, graph = _call(f"{base_url}/graph", token=TOKEN)
        assert graph["documents"][0]["payload"] == {"title": "My Book"}
        assert (tmp_path / "book.md").read_text(encoding="utf-8") == "# My Book\n"

        assert _call(f"{base_url}/save", method="POST", token=TOKEN, payload={"doc": "book", "payload": {"title": "Allowed"}})[0] == 200
    finally:
        server.shutdown()
        server.server_close()


def test_options_preflight_is_exempt_from_auth(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, base_url = _serve(store, token=TOKEN)
    try:
        assert _call(f"{base_url}/save", method="OPTIONS")[0] == 204
    finally:
        server.shutdown()
        server.server_close()


def test_env_var_configures_the_token_when_the_flag_is_absent(tmp_path: Path, monkeypatch) -> None:
    from sldb.cli.serve.auth import resolve_token

    monkeypatch.delenv("SLDB_SERVE_TOKEN", raising=False)
    assert resolve_token(None) is None
    monkeypatch.setenv("SLDB_SERVE_TOKEN", TOKEN)
    assert resolve_token(None) == TOKEN
    assert resolve_token("flag-wins") == "flag-wins"

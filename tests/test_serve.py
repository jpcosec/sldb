from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from sldb.cli.serve import save_routes
from sldb.cli.serve.http_server import build_handler
from sldb.store.io import load_store_index
from tests.store.test_cli_store import _PY_ARGS, _doc_track, _init, _model_add


JSON_HEADERS = {"Content-Type": "application/json"}


def _hash_d(payload: dict) -> str:
    """The version a client sees: sha256 of the payload JSON, sorted keys (== store hash_d)."""
    import hashlib
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def test_serve_endpoints_use_real_store(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    pythonpath = _PY_ARGS[1]
    handler = build_handler(str(store), pythonpath, cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        health_status, health = _request_json(f"{base_url}/health")
        assert health_status == 200
        assert health == {"status": "ok"}

        schema_status, schema = _request_json(f"{base_url}/schema")
        assert schema_status == 200
        assert schema["models"] == [
            {
                "id": "SimpleBook",
                "model_ref": "tests.store.test_cli_store:SimpleBook",
                "fields": [
                    {"name": "title", "kind": "string", "required": True}
                ],
                "containment": {},
                "references": [],
                "semantics": {"representation": ["markdown"], "source": ["document", "markdown"]},
                "template": "# ⸢rev•title⸥",
            }
        ]

        graph_status, graph = _request_json(f"{base_url}/graph")
        assert graph_status == 200
        assert graph["documents"] == [
            {
                "id": "book",
                "model_name": "SimpleBook",
                "path": "book.md",
                "version": _hash_d({"title": "My Book"}),
                "payload": {"title": "My Book"},
                "semantic_tags": ["representation.markdown", "source.document.markdown"],
            }
        ]

        save_status, save = _request_json(
            f"{base_url}/save",
            method="POST",
            payload={"doc": "book", "payload": {"title": "Updated Title"}},
        )
        assert save_status == 200
        assert save == {"ok": True, "doc": "book"}

        graph_after_status, graph_after = _request_json(f"{base_url}/graph")
        assert graph_after_status == 200
        assert graph_after["documents"][0]["payload"] == {"title": "Updated Title"}
        assert graph_after["documents"][0]["version"] == _hash_d({"title": "Updated Title"})
        assert graph_after["documents"][0]["version"] != graph["documents"][0]["version"]
        assert (tmp_path / "book.md").read_text(encoding="utf-8") == "# Updated Title\n"

        missing_status, missing = _request_json(
            f"{base_url}/save",
            method="POST",
            payload={"doc": "missing", "payload": {"title": "Nope"}},
            expected_error=404,
        )
        assert missing_status == 404
        assert missing == {"ok": False, "error": "Unknown doc: missing"}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_edges_endpoints_use_real_api(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    handler = build_handler(str(store), _PY_ARGS[1], cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        status, edges = _request_json(f"{base_url}/edges?from=SimpleBook:book")
        assert status == 200
        assert {edge["relation"] for edge in edges["edges"]} == {"has_section", "tagged_as"}

        status, incoming = _request_json(f"{base_url}/edges?to=SimpleBook:book")
        assert status == 200
        assert [edge["relation"] for edge in incoming["edges"]] == ["has_document"]

        status, filtered = _request_json(f"{base_url}/edges?from=SimpleBook:book&relation=tagged_as")
        assert status == 200
        assert {edge["relation"] for edge in filtered["edges"]} == {"tagged_as"}

        status, node = _request_json(f"{base_url}/edges/node?id=SimpleBook:book")
        assert status == 200
        assert node["node"]["node_type"] == "SimpleBook"

        status, nodes = _request_json(f"{base_url}/edges/nodes?type=sldb_model")
        assert status == 200
        assert [(node["id"], node["node_type"]) for node in nodes["nodes"]] == [("sldb://model/SimpleBook", "sldb_model")]

        status, missing = _request_json(f"{base_url}/edges?from=", expected_error=400)
        assert status == 400
        assert missing == {"ok": False, "error": "Missing parameter: expected 'from' or 'to'"}

        status, unknown = _request_json(f"{base_url}/edges/node?id=nope", expected_error=404)
        assert status == 404
        assert unknown == {"ok": False, "error": "Unknown node: nope"}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_graph_endpoints_use_real_api(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    handler = build_handler(str(store), _PY_ARGS[1], cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        status, cycles = _request_json(f"{base_url}/graph/cycles")
        assert status == 200
        assert cycles == {"cycles": []}

        status, components = _request_json(f"{base_url}/graph/components")
        assert status == 200
        assert "sldb://document/SimpleBook:book" in components["components"][0]

        status, central = _request_json(f"{base_url}/graph/central?limit=5")
        assert status == 200
        assert len(central["central"]) == 5
        assert all(sorted(item) == ["node", "score"] for item in central["central"])

        status, isolated = _request_json(f"{base_url}/graph/isolated")
        assert status == 200
        assert isolated == {"isolated": []}

        status, neighborhood = _request_json(f"{base_url}/graph/neighborhood?node=SimpleBook:book")
        assert status == 200
        assert "sldb://section/SimpleBook:book#my-book" in neighborhood["nodes"]

        status, path = _request_json(f"{base_url}/graph/path?source=sldb://model/SimpleBook&target=sldb://section/SimpleBook:book%23my-book")
        assert status == 200
        assert path["path"][0] == "sldb://model/SimpleBook"

        status, missing = _request_json(f"{base_url}/graph/neighborhood", expected_error=400)
        assert status == 400
        assert missing["ok"] is False
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_batch_save_create_update_delete(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    _track_other(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "book", "action": "update", "model": "SimpleBook", "payload": {"title": "Batch Updated"}, "expected": {"title": "My Book"}},
            {"id": "other", "action": "delete", "expected": {"title": "Other Book"}},
            {"id": "book2", "action": "create", "model": "SimpleBook", "payload": {"title": "Batch New"}},
        ]})
        assert status == 200
        # create applied before update before delete, regardless of request order
        assert body == {"ok": True, "saved": ["book2", "book", "other"]}
        _, graph = _request_json(f"{base_url}/graph")
        ids = [doc["id"] for doc in graph["documents"]]
        assert "other" not in ids
        book = next(doc for doc in graph["documents"] if doc["id"] == "book")
        assert book["payload"] == {"title": "Batch Updated"}
        assert next(doc for doc in graph["documents"] if doc["id"] == "book2")["model_name"] == "SimpleBook"
        assert (tmp_path / "book2.md").read_text(encoding="utf-8") == "# Batch New\n"
        assert (tmp_path / "other.md").read_text(encoding="utf-8") == "# Other Book\n"
    finally:
        _stop(server, thread)


def test_batch_save_stale_expected_conflict(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "book", "action": "update", "model": "SimpleBook", "payload": {"title": "X"}, "expected": {"title": "OLD"}},
        ]}, expected_error=409)
        assert status == 409
        assert body == {"ok": False, "error": "book cambió en SLDB. Recarga para evitar sobrescribirlo."}
        _, graph = _request_json(f"{base_url}/graph")
        assert next(doc for doc in graph["documents"] if doc["id"] == "book")["payload"] == {"title": "My Book"}
    finally:
        _stop(server, thread)


def test_batch_save_duplicate_create_rejected(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "book", "action": "create", "model": "SimpleBook", "payload": {"title": "Nope"}},
        ]}, expected_error=409)
        assert status == 409
        assert body == {"ok": False, "error": "Ya existe el documento book."}
        (tmp_path / "taken.md").write_text("# Taken\n", encoding="utf-8")
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "taken", "action": "create", "model": "SimpleBook", "payload": {"title": "Nope"}},
        ]}, expected_error=409)
        assert status == 409
        assert body == {"ok": False, "error": "El archivo de taken ya existe; elige otro ID."}
    finally:
        _stop(server, thread)


def test_batch_save_invalid_payload_422(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "bad", "action": "create", "model": "SimpleBook", "payload": {"title": 123}},
        ]}, expected_error=422)
        assert status == 422
        assert body["ok"] is False
        assert "validation error" in body["error"]
        assert not (tmp_path / "bad.md").exists()
    finally:
        _stop(server, thread)


def test_batch_save_partial_failure_reports_completed(tmp_path: Path, monkeypatch: Any) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    calls = {"n": 0}
    real_create = save_routes.create_document

    def flaky(store: Path, model: str, path: Path, payload: dict, **kw: Any) -> Any:
        calls["n"] += 1
        if calls["n"] == 2:
            raise RuntimeError("boom")
        return real_create(store, model, path, payload, **kw)

    monkeypatch.setattr(save_routes, "create_document", flaky)
    try:
        status, body = _request_json(f"{base_url}/save", method="POST", payload={"changes": [
            {"id": "c1", "action": "create", "model": "SimpleBook", "payload": {"title": "1"}},
            {"id": "c2", "action": "create", "model": "SimpleBook", "payload": {"title": "2"}},
            {"id": "c3", "action": "create", "model": "SimpleBook", "payload": {"title": "3"}},
        ]}, expected_error=500)
        assert status == 500
        assert body == {"ok": False, "error": "No se completó el guardado: boom", "completed": ["c1"]}
        assert (tmp_path / "c1.md").read_text(encoding="utf-8") == "# 1\n"
        assert not (tmp_path / "c3.md").exists()
    finally:
        _stop(server, thread)


def _track_other(tmp_path: Path) -> None:
    other = tmp_path / "other.md"
    other.write_text("# Other Book\n", encoding="utf-8")
    _doc_track(tmp_path, other)


def _serve(store: Path) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    handler = build_handler(str(store), _PY_ARGS[1], cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_address[1]}"


def _stop(server: ThreadingHTTPServer, thread: threading.Thread) -> None:
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


def _build_store(tmp_path: Path) -> Path:
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    return tmp_path / ".sldb"


def _request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    expected_error: int | None = None,
) -> tuple[int, dict]:
    request = Request(url, method=method)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        for name, value in JSON_HEADERS.items():
            request.add_header(name, value)
    try:
        with urlopen(request, data=data, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if expected_error != exc.code:
            raise
        return exc.code, json.loads(exc.read().decode("utf-8"))


# ── /models* (model lifecycle) y /lint: añadidos por la autoridad HTTP ──────

def _build_gadget_store(tmp_path: Path) -> tuple[Path, str]:
    """Store con un modelo propio en tmp_path: los drafts viven junto al módulo, así no tocan los de otros tests."""
    from sldb.cli import main as cli_main

    module = tmp_path / "kb_gadget.py"
    module.write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Gadget(StructuredNLDoc):\n"
        '    __template__ = "# \u2e22rev\u2022title\u2e25"\n'
        '    title: str = Field(description="Title.")\n',
        encoding="utf-8",
    )
    _init(tmp_path)
    cli_main(["models", "add", "kb_gadget:Gadget", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    doc = tmp_path / "gadget-1.md"
    doc.write_text("# Widget\n", encoding="utf-8")
    cli_main(["docs", "track", str(doc), "--model", "Gadget", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    return tmp_path / ".sldb", str(tmp_path)


def test_schema_includes_model_graph_dunders(tmp_path: Path) -> None:
    """GET /schema expone containment/references/semantics/template y defaults declarados.

    Los modelos que no declaran un dunder heredan el default de StructuredNLDoc;
    los campos con default_factory omiten la clave ``default``; un default
    explícito ``None`` sí aparece.
    """
    import sys

    store, module_pythonpath = _build_graphdoc_store(tmp_path)
    server, thread, base_url = _serve_with_pythonpath(store, module_pythonpath)
    sys.modules.pop("kb_graphdoc", None)
    try:
        status, schema = _request_json(f"{base_url}/schema")
        assert status == 200
        rich = next(model for model in schema["models"] if model["id"] == "RichBook")
        assert rich["containment"] == {"chapters": ["ChapterDoc"], "notes": ["NoteDoc"]}
        assert rich["references"] == ["owner_id", "related"]
        assert rich["semantics"] == {"type": ["book"], "workspace": ["library"]}
        assert rich["template"] == "# ⸢rev•title⸥"
        fields = {field["name"]: field for field in rich["fields"]}
        assert "default" not in fields["title"]
        assert fields["level"]["default"] == "low"
        assert "default" not in fields["tags"]
        assert fields["owner_id"]["default"] is None

        bare = next(model for model in schema["models"] if model["id"] == "PlainBook")
        assert bare["containment"] == {}
        assert bare["references"] == []
        assert bare["semantics"] == {"representation": ["markdown"], "source": ["document", "markdown"]}
        assert bare["template"] == ""
    finally:
        _stop(server, thread)
        sys.modules.pop("kb_graphdoc", None)


def _build_graphdoc_store(tmp_path: Path) -> tuple[Path, str]:
    """Store con un modelo rico en dunders de grafo y un modelo pelado."""
    from sldb.cli import main as cli_main

    module = tmp_path / "kb_graphdoc.py"
    module.write_text(
        "from enum import StrEnum\n"
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Level(StrEnum):\n"
        '    LOW = "low"\n'
        '    HIGH = "high"\n\n'
        "class RichBook(StructuredNLDoc):\n"
        '    __containment__ = {"chapters": ["ChapterDoc"], "notes": ["NoteDoc"]}\n'
        '    __references__ = ["owner_id", "related"]\n'
        '    __semantics__ = {"type": ["book"], "workspace": ["library"]}\n'
        '    __template__ = "# \u2e22rev\u2022title\u2e25"\n'
        '    title: str = Field(description="Title.")\n'
        '    level: Level = Field(default=Level.LOW, description="Level.")\n'
        '    tags: list[str] = Field(default_factory=list, description="Tags.")\n'
        '    owner_id: str | None = Field(default=None, description="Owner.")\n',
        encoding="utf-8",
    )
    plain = tmp_path / "kb_plaindoc.py"
    plain.write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class PlainBook(StructuredNLDoc):\n"
        '    title: str = Field(description="Title.")\n',
        encoding="utf-8",
    )
    _init(tmp_path)
    cli_main(["models", "add", "kb_graphdoc:RichBook", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    cli_main(["models", "add", "kb_plaindoc:PlainBook", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    return tmp_path / ".sldb", str(tmp_path)


def _serve_with_pythonpath(store: Path, pythonpath: str) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    handler = build_handler(str(store), pythonpath, cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_address[1]}"


def test_models_endpoints_use_native_api(tmp_path: Path) -> None:
    import sys

    store, module_pythonpath = _build_gadget_store(tmp_path)
    sys.modules.pop("kb_gadget", None)
    server, thread, base_url = _serve_with_pythonpath(store, module_pythonpath)
    try:
        status, catalog = _request_json(f"{base_url}/models")
        assert status == 200
        gadget = next(model for model in catalog["models"] if model["name"] == "Gadget")
        assert gadget["model_ref"] == "kb_gadget:Gadget"
        assert (gadget["version"], gadget["documents"]) == (1, 1)

        status, detail = _request_json(f"{base_url}/models/detail?model=Gadget")
        assert status == 200 and detail["ok"] is True
        assert {field["name"] for field in detail["model"]["fields"]} == {"title"}
        assert detail["model"]["version"] == 1

        # modelo inexistente: error de dominio en HTTP 200, no un 500
        status, missing = _request_json(f"{base_url}/models/detail?model=Nope")
        assert status == 200 and missing["ok"] is False and "Nope" in missing["error"]

        # parámetro faltante: 400
        status, bad = _request_json(f"{base_url}/models/detail", expected_error=400)
        assert status == 400 and bad["ok"] is False

        status, added = _request_json(
            f"{base_url}/models/fields-add",
            method="POST",
            payload={"model": "Gadget", "field_name": "price", "field_type": "int", "description": "Precio.", "default": "5"},
        )
        assert status == 200 and added["ok"] is True
        assert added["draft_path"].endswith("kb_gadget.py.temp")
        # el draft es un .py.temp junto al módulo; el modelo activo no cambió
        assert (tmp_path / "kb_gadget.py.temp").exists()
        assert "price" not in (tmp_path / "kb_gadget.py").read_text(encoding="utf-8")

        status, validated = _request_json(f"{base_url}/models/validate", method="POST", payload={"model": "Gadget"})
        assert status == 200 and validated["ok"] is True
        assert (validated["valid"], validated["draft"], validated["promoted"]) == (True, True, False)

        status, promoted = _request_json(f"{base_url}/models/promote", method="POST", payload={"model": "Gadget"})
        assert status == 200 and promoted["ok"] is True
        assert (promoted["promoted"], promoted["version"]) == (True, 2)
        assert not (tmp_path / "kb_gadget.py.temp").exists()
        assert "price" in (tmp_path / "kb_gadget.py").read_text(encoding="utf-8")

        # promover sin draft: error de dominio, no 500
        status, again = _request_json(f"{base_url}/models/promote", method="POST", payload={"model": "Gadget"})
        assert status == 200 and again["ok"] is False
        assert "draft" in again["error"]

        status, no_field = _request_json(
            f"{base_url}/models/fields-remove", method="POST", payload={"model": "Gadget"}, expected_error=400
        )
        assert status == 400 and no_field["ok"] is False

        status, edited = _request_json(
            f"{base_url}/models/template-edit",
            method="POST",
            payload={"model": "Gadget", "content": "# \u2e22rev\u2022title\u2e25\n"},
        )
        assert status == 200 and edited["ok"] is True
    finally:
        _stop(server, thread)
        sys.modules.pop("kb_gadget", None)


def test_lint_endpoints_use_real_api(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, lint = _request_json(f"{base_url}/lint")
        assert status == 200
        assert lint["count"] == len(lint["problems"])
        for problem in lint["problems"]:
            assert set(problem) == {"kind", "severity", "doc", "detail"}
        # store fresco sin `edges init`: shards con relación no registrada
        assert any(p["kind"] == "edge" and p["severity"] == "error" for p in lint["problems"])

        # mutar el doc y añadir un enlace roto: aparecen problemas store y link
        (tmp_path / "book.md").write_text("# My Book\n\nSee [[nope]]\n", encoding="utf-8")
        status, lint = _request_json(f"{base_url}/lint")
        assert status == 200
        store_problems = [p for p in lint["problems"] if p["kind"] == "store" and p["doc"] == "book"]
        assert any(p["severity"] == "warning" for p in store_problems)
        link_problems = [p for p in lint["problems"] if p["kind"] == "link" and p["doc"] == "book"]
        assert any("nope" in p["detail"] for p in link_problems)
    finally:
        _stop(server, thread)



def test_document_endpoint_returns_full_ir(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/document?id=book")
        assert status == 200
        assert body["id"] == "book"
        assert body["model_name"] == "SimpleBook"
        assert body["path"] == "book.md"
        assert body["payload"] == {"title": "My Book"}
        assert body["semantic_tags"] == ["representation.markdown", "source.document.markdown"]
        ir = body["ir"]
        assert sorted(ir) == ["context", "context_index", "graph", "nodes", "structure", "surface"]
        assert ir["context"]["semantic"] == {"model": "SimpleBook", "tags": body["semantic_tags"]}
        assert ir["structure"][0]["title"] == "My Book"
        assert "span" in ir["structure"][0]
        assert ir["surface"][0]["kind"] == "heading"
        assert ir["graph"]["nodes"][0]["kind"] == "document"
    finally:
        _stop(server, thread)


def test_document_ir_endpoint_returns_only_ir(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, doc = _request_json(f"{base_url}/document?id=book")
        assert status == 200
        status, ir = _request_json(f"{base_url}/document/ir?id=book")
        assert status == 200
        assert ir == doc["ir"]
        assert "id" not in ir and "payload" not in ir
    finally:
        _stop(server, thread)


def test_document_unknown_doc_returns_404(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/document?id=nope", expected_error=404)
        assert status == 404
        assert body == {"ok": False, "error": "Unknown doc: nope"}

        status, body = _request_json(f"{base_url}/document/ir?id=nope", expected_error=404)
        assert status == 404
    finally:
        _stop(server, thread)


def test_document_missing_id_returns_400(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/document", expected_error=400)
        assert status == 400
        assert body == {"ok": False, "error": "Missing parameter: id"}
    finally:
        _stop(server, thread)


def test_document_unbuildable_ir_returns_422(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, _ = _request_json(f"{base_url}/document?id=book")
        assert status == 200
        # romper el roundtrip: el markdown ya no extrae al modelo -> IR no construible
        (tmp_path / "book.md").write_text("no longer a book\n", encoding="utf-8")
        status, body = _request_json(f"{base_url}/document?id=book", expected_error=422)
        assert status == 422
        assert body["ok"] is False
        assert "title" in body["error"]
    finally:
        _stop(server, thread)


# ── /docs* (document lifecycle) ────────────────────────────────────────────────

def test_docs_create_tracks_and_returns_version(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/create", method="POST", payload={"model": "SimpleBook", "name": "newbook", "payload": {"title": "New Book"}})
        assert status == 200
        assert body["ok"] is True
        assert body["doc"]["id"] == "newbook"
        assert body["doc"]["model_name"] == "SimpleBook"
        assert body["doc"]["path"] == "newbook.md"
        assert body["doc"]["version"] == _hash_d({"title": "New Book"})
        assert (tmp_path / "newbook.md").read_text(encoding="utf-8") == "# New Book\n"
        _, graph = _request_json(f"{base_url}/graph")
        assert {doc["id"] for doc in graph["documents"]} == {"book", "newbook"}
    finally:
        _stop(server, thread)


def test_docs_create_duplicate_conflict(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/create", method="POST", payload={"model": "SimpleBook", "name": "book", "payload": {"title": "Nope"}}, expected_error=409)
        assert status == 409
        assert body == {"ok": False, "error": "Ya existe el documento book."}
    finally:
        _stop(server, thread)


def test_docs_create_invalid_payload_422(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/create", method="POST", payload={"model": "SimpleBook", "name": "bad", "payload": {"title": 123}}, expected_error=422)
        assert status == 422
        assert body["ok"] is False
        assert "validation error" in body["error"]
        assert not (tmp_path / "bad.md").exists()
    finally:
        _stop(server, thread)


def test_docs_create_target_file_conflict(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        (tmp_path / "taken.md").write_text("# Taken\n", encoding="utf-8")
        status, body = _request_json(f"{base_url}/docs/create", method="POST", payload={"model": "SimpleBook", "name": "taken", "payload": {"title": "Nope"}}, expected_error=409)
        assert status == 409
        assert body == {"ok": False, "error": "El archivo de taken ya existe; elige otro ID."}
    finally:
        _stop(server, thread)


def test_docs_create_unregistered_model_404(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/create", method="POST", payload={"model": "Nope", "name": "other", "payload": {"title": "X"}}, expected_error=404)
        assert status == 404
        assert body["ok"] is False
        assert "Nope" in body["error"]
    finally:
        _stop(server, thread)


def test_docs_track_existing_file(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        (tmp_path / "loose.md").write_text("# Loose Book\n", encoding="utf-8")
        status, body = _request_json(f"{base_url}/docs/track", method="POST", payload={"model": "SimpleBook", "path": "loose.md"})
        assert status == 200
        assert body["ok"] is True
        assert body["doc"]["id"] == "loose"
        assert body["doc"]["version"] == _hash_d({"title": "Loose Book"})
        _, graph = _request_json(f"{base_url}/graph")
        assert {doc["id"] for doc in graph["documents"]} == {"book", "loose"}
    finally:
        _stop(server, thread)


def test_docs_track_missing_path_404(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/track", method="POST", payload={"model": "SimpleBook", "path": "nope.md"}, expected_error=404)
        assert status == 404
        assert body["ok"] is False
        assert "nope.md" in body["error"]
    finally:
        _stop(server, thread)


def test_docs_untrack_keeps_file_on_disk(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/untrack", method="POST", payload={"name": "book"})
        assert status == 200
        assert body["ok"] is True
        assert body["doc"]["id"] == "book"
        assert body["doc"]["path"] == "book.md"
        assert body["doc"]["version"] == _hash_d({"title": "My Book"})
        assert (tmp_path / "book.md").read_text(encoding="utf-8") == "# My Book\n"
        _, graph = _request_json(f"{base_url}/graph")
        assert "book" not in {doc["id"] for doc in graph["documents"]}
    finally:
        _stop(server, thread)


def test_docs_untrack_missing_doc_404(tmp_path: Path) -> None:
    store = _build_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/docs/untrack", method="POST", payload={"name": "ghost"}, expected_error=404)
        assert status == 404
        assert body == {"ok": False, "error": "Doc 'ghost' not found."}
    finally:
        _stop(server, thread)


def _build_relpkg_store(tmp_path: Path) -> tuple[Path, str]:
    """Store con un modelo en un paquete donde un módulo importa de su hermano por import RELATIVO.

    Es el patrón de AgentsKBs (kb_models/knowledge/rule.py -> from .index_proxies import ...):
    si un endpoint resolviera el modelo por ruta de archivo (nombre de módulo derivado del
    paquete padre), el import relativo rompe con 'No module named <parent>.sibling'.
    """
    from sldb.cli import main as cli_main

    pkg = tmp_path / "kb_models_rel"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "sibling.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class RelBase(StructuredNLDoc):\n"
        '    __template__ = "# \u2e22rev\u2022title\u2e25"\n'
        '    title: str = Field(description="Title.")\n',
        encoding="utf-8",
    )
    (pkg / "relbook.py").write_text(
        "from pydantic import Field\n"
        "from .sibling import RelBase\n\n"
        "class RelBook(RelBase):\n"
        '    author: str = Field(default="", description="Author.")\n',
        encoding="utf-8",
    )
    _init(tmp_path)
    cli_main(["models", "add", "kb_models_rel.relbook:RelBook", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    doc = tmp_path / "rel-book.md"
    doc.write_text("# The Rel Book\n", encoding="utf-8")
    cli_main(["docs", "track", str(doc), "--model", "RelBook", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)])
    return tmp_path / ".sldb", str(tmp_path)


def test_models_endpoints_resolve_relative_imports_by_package_name(tmp_path: Path) -> None:
    """Los cuatro endpoints resuelven el modelo EXACTAMENTE igual: por nombre de paquete.

    Regresión del bug 'No module named kb_models.index_proxies': un loader por ruta de
    archivo rompe `from .sibling import ...`; todos estos endpoints deben dar 200.
    """
    import sys

    store, module_pythonpath = _build_relpkg_store(tmp_path)
    for name in ("kb_models_rel", "kb_models_rel.sibling", "kb_models_rel.relbook"):
        sys.modules.pop(name, None)
    server, thread, base_url = _serve_with_pythonpath(store, module_pythonpath)
    try:
        status, catalog = _request_json(f"{base_url}/models")
        assert status == 200
        assert next(m for m in catalog["models"] if m["name"] == "RelBook")["model_ref"] == "kb_models_rel.relbook:RelBook"

        status, detail = _request_json(f"{base_url}/models/detail?model=RelBook")
        assert status == 200 and detail["ok"] is True
        assert {f["name"] for f in detail["model"]["fields"]} == {"title", "author"}

        status, schema = _request_json(f"{base_url}/schema")
        assert status == 200
        assert next(m for m in schema["models"] if m["id"] == "RelBook")["template"] == "# ⸢rev•title⸥"

        status, graph = _request_json(f"{base_url}/graph")
        assert status == 200
        assert graph["documents"][0] == {
            "id": "rel-book",
            "model_name": "RelBook",
            "path": "rel-book.md",
            "version": _hash_d({"title": "The Rel Book", "author": ""}),
            "payload": {"title": "The Rel Book", "author": ""},
            "semantic_tags": ["representation.markdown", "source.document.markdown"],
        }
    finally:
        _stop(server, thread)
        for name in ("kb_models_rel", "kb_models_rel.sibling", "kb_models_rel.relbook"):
            sys.modules.pop(name, None)


# ── Surfaces de lectura (V1 Store Explorer / V4 / V5 / V7 / V9) ─────────────

def _build_chapter_store(tmp_path: Path) -> Path:
    """Store con un segundo doc con secciones para los endpoints de lectura."""
    store = _build_store(tmp_path)
    doc = tmp_path / "guide.md"
    doc.write_text("# My Book\n\n## Setup\n\nSet it up.\n", encoding="utf-8")
    _doc_track(tmp_path, doc, name="guide")
    return store


def test_stores_describe_current_store(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/stores")
        assert status == 200
        assert body == {
            "store": str(store),
            "root": str(tmp_path),
            "model_count": 1,
            "doc_count": 2,
            "hash_a": load_store_index(store).hash_a,
            "stores": [],
        }
    finally:
        _stop(server, thread)


def test_stores_check_reports_mismatched_hash_c(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    guide = tmp_path / "guide.md"
    guide.write_text("# My Book\n\n## Setup\n\nMutated.\n", encoding="utf-8")
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/stores/check")
        assert status == 200
        assert body["ok"] is False
        assert body["checked"] == 2
        entry = next(item for item in body["mismatched"] if item["doc"] == "guide")
        assert entry["kind"] == "hash_c"
        assert entry["expected"] != entry["actual"]
        assert len(entry["actual"]) == 64
    finally:
        _stop(server, thread)


def test_fields_list_and_single_path(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/fields?doc=book")
        assert status == 200
        assert body["doc"] == "book" and body["model"] == "SimpleBook"
        title = next(f for f in body["fields"] if f["name"] == "title")
        assert title["value"] == "My Book"
        assert title["is_required"] and title["is_list"] is False

        status, body = _request_json(f"{base_url}/fields?doc=book&path=title")
        assert status == 200
        assert body == {"doc": "book", "model": "SimpleBook", "path": "title", "value": "My Book", "type": "str", "is_list": False, "is_required": True, "is_reference": False}

        status, body = _request_json(f"{base_url}/fields?doc=book&path=missing", expected_error=404)
        assert status == 404 and body["ok"] is False
    finally:
        _stop(server, thread)


def test_sections_from_ir_context_index(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/sections?doc=guide")
        assert status == 200
        assert body["doc"] == "guide"
        setup = next(s for s in body["sections"] if s["title"] == "Setup")
        assert setup["path"] == "my-book/setup"
        assert isinstance(setup["field_paths"], list)
    finally:
        _stop(server, thread)


def test_ast_exposes_full_ir_and_sections(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/ast?doc=guide")
        assert status == 200
        doc = body["document"]
        assert doc["name"] == "guide" and doc["model"] == "SimpleBook"
        assert doc["payload"] == {"title": "My Book"}
        assert any(section["title"] == "Setup" for section in doc["sections"])
        assert "structure" in doc["ir"] and "surface" in doc["ir"]
    finally:
        _stop(server, thread)


def test_extract_and_render(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/extract?doc=book")
        assert status == 200 and body == {"doc": "book", "payload": {"title": "My Book"}}

        status, body = _request_json(f"{base_url}/render?doc=book")
        assert status == 200 and body["markdown"] == "# My Book"

        status, body = _request_json(f"{base_url}/render?model=SimpleBook")
        assert status == 200 and body["template"] == "# ⸢rev•title⸥"
    finally:
        _stop(server, thread)


def test_reader_routes_validate_params(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/fields", expected_error=400)
        assert status == 400 and "doc" in body["error"]

        status, body = _request_json(f"{base_url}/sections?doc=ghost", expected_error=404)
        assert status == 404 and body["ok"] is False

        status, body = _request_json(f"{base_url}/ast?doc=ghost", expected_error=404)
        assert status == 404 and body["ok"] is False

        status, body = _request_json(f"{base_url}/render?doc=ghost", expected_error=404)
        assert status == 404 and body["ok"] is False

        status, body = _request_json(f"{base_url}/render?doc=book&format=html")
        assert status == 200 and body["markdown"] == "# My Book"
    finally:
        _stop(server, thread)


# ── GET /find: la búsqueda del CLI expuesta sobre HTTP ──────────────────────

def test_find_physical_search(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/find?q=book&in=physical&type=doc")
        assert status == 200
        names = [result["name"] for result in body["results"]]
        assert "book" in names
        assert all(result["kind"] == "doc" for result in body["results"])
    finally:
        _stop(server, thread)


def test_find_semantic_search(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/find?q=markdown&in=semantic&type=doc")
        assert status == 200
        names = [result["name"] for result in body["results"]]
        assert "book" in names and "guide" in names
    finally:
        _stop(server, thread)


def test_find_where_predicate_filters_and_invalid_where_is_400(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        url = f"{base_url}/find?q=book&in=physical&type=doc&where={quote('has(title)')}"
        status, body = _request_json(url)
        assert status == 200
        assert body["results"] and body["results"][0]["name"] == "book"

        status, body = _request_json(f"{base_url}/find?q=book&in=physical&where=nonsense(missing", expected_error=400)
        assert status == 400
        assert "no evaluator understands" in body["error"]
    finally:
        _stop(server, thread)


def test_find_limit_and_select(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/find?q=markdown&in=semantic&limit=2")
        assert status == 200
        assert len(body["results"]) == 2

        status, body = _request_json(f"{base_url}/find?q=book&in=physical&type=doc&select=kind,name,doc")
        assert status == 200
        assert set(body["results"][0].keys()) == {"kind", "name", "doc"}
    finally:
        _stop(server, thread)


def test_find_flags_and_param_validation(tmp_path: Path) -> None:
    store = _build_chapter_store(tmp_path)
    server, thread, base_url = _serve(store)
    try:
        status, body = _request_json(f"{base_url}/find?q=bok&in=physical&type=doc&fuzzy=1")
        assert status == 200
        names = [result["name"] for result in body["results"]]
        assert "book" in names

        status, body = _request_json(f"{base_url}/find?q=book&in=bogus", expected_error=400)
        assert status == 400 and "Invalid parameter in" in body["error"]

        status, body = _request_json(f"{base_url}/find?q=book&type=bogus", expected_error=400)
        assert status == 400 and "Invalid parameter type" in body["error"]

        status, body = _request_json(f"{base_url}/find?q=book&limit=abc", expected_error=400)
        assert status == 400 and "Invalid parameter limit" in body["error"]

        status, body = _request_json(f"{base_url}/find", expected_error=400)
        assert status == 400 and "Missing parameter: q" in body["error"]
    finally:
        _stop(server, thread)

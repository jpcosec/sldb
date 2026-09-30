"""GET /edges (document-to-document view) and POST /docs, over a real served store."""

from __future__ import annotations

import sys
from pathlib import Path

from sldb.api import add_model, create_document, init_relations
from tests.store.test_cli_store import _init
from tests.test_serve import _request_json, _serve, _stop

_MODELS = '''
from __future__ import annotations
from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class ItemDoc(StructuredNLDoc):
    __references__ = ["source"]
    __template__ = "# ⸢rev•title⸥\\n\\nfrom: ⸢rev•source⸥"
    title: str = Field(description="Title.")
    source: str = Field(description="Export id of the note.")
'''


def _edge_store(tmp_path: Path) -> tuple[Path, str]:
    (tmp_path / "kb_edges.py").write_text(_MODELS, encoding="utf-8")
    _init(tmp_path)
    store, py = tmp_path / ".sldb", str(tmp_path)
    for name in ("NoteDoc", "ItemDoc"):
        add_model(store, f"kb_edges:{name}", py)
    init_relations(store, py)
    create_document(store, "NoteDoc", tmp_path / "n1.md", {"title": "N"}, name="n1", pythonpath=py)
    create_document(store, "ItemDoc", tmp_path / "i1.md", {"title": "I", "source": "NoteDoc:n1"}, name="i1", pythonpath=py)
    return store, py


def _serve_at(store: Path, py: str):
    server, thread, base = _serve(store)
    server.RequestHandlerClass.pythonpath = py
    return server, thread, base


def test_edges_lists_document_edges_and_filters_by_id(tmp_path: Path) -> None:
    store, py = _edge_store(tmp_path)
    server, thread, base = _serve_at(store, py)
    try:
        status, body = _request_json(f"{base}/edges")
        assert status == 200
        assert body["edges"] == [{"id": "references:ItemDoc:i1>NoteDoc:n1", "source": "ItemDoc:i1", "target": "NoteDoc:n1", "type": "references", "origin": "schema", "relationDoc": None}]
        _, mine = _request_json(f"{base}/edges?id=NoteDoc:n1")
        _, other = _request_json(f"{base}/edges?id=NoteDoc:zzz")
        assert len(mine["edges"]) == 1 and other["edges"] == []
    finally:
        _stop(server, thread)


def test_docs_creates_a_tracked_document(tmp_path: Path) -> None:
    store, py = _edge_store(tmp_path)
    server, thread, base = _serve_at(store, py)
    try:
        status, body = _request_json(f"{base}/docs", method="POST", payload={"model": "ItemDoc", "name": "i2", "payload": {"title": "J", "source": "NoteDoc:n1"}})
        assert status == 200 and body["ok"] is True and body["id"] == "i2" and body["version"]
        _, graph = _request_json(f"{base}/graph")
        assert "i2" in [doc["id"] for doc in graph["documents"]]
        _, edges = _request_json(f"{base}/edges?id=ItemDoc:i2")
        assert [edge["target"] for edge in edges["edges"]] == ["NoteDoc:n1"]
    finally:
        _stop(server, thread)


def test_docs_reports_each_failure_with_its_status(tmp_path: Path) -> None:
    store, py = _edge_store(tmp_path)
    server, thread, base = _serve_at(store, py)
    good = {"model": "NoteDoc", "name": "n2", "payload": {"title": "M"}}
    try:
        for payload, code in [({"model": "NoteDoc"}, 400), ({**good, "model": "Nope"}, 404), ({**good, "name": "n1"}, 409), ({**good, "payload": {"wrong": 1}}, 422)]:
            status, body = _request_json(f"{base}/docs", method="POST", payload=payload, expected_error=code)
            assert status == code and body["ok"] is False and body["error"]
    finally:
        _stop(server, thread)

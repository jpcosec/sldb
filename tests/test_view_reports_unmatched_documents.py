"""A view lists the documents no glyph matches as gaps instead of failing; `strict` keeps the failure."""

from __future__ import annotations

import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from sldb.api import evaluate_projection_view, resolve_documents, resolve_view
from sldb.api.notations import ViewError
from sldb.cli.serve.http_server import build_handler
from tests.notations.test_notation_view_and_routes import (
    _create_sample_spec_and_nodes,
    _request_json,
    test_store,  # noqa: F401  (fixture)
)

NODES = ["SpecNodeDoc:spec1.User", "SpecNodeDoc:spec1.Order"]
GAP = "SpecDoc:spec1"
VIEW = {
    "nodes": [{"model": "SpecNodeDoc"}, {"model": "SpecDoc"}],
    "relations": ["association"],
    "direction": "both",
    "notation": "NotationDoc:uml-class",
}


def test_projection_lists_the_unmatched_document_as_gap(test_store: Path):
    _create_sample_spec_and_nodes(test_store)
    result = evaluate_projection_view(test_store, VIEW)
    assert result["gaps"] == [{"id": GAP, "model": "SpecDoc"}]
    assert {"SpecNodeDoc:spec1.User", "SpecNodeDoc:spec1.Order"} <= {f"{n['model']}:{n['name']}" for n in result["nodes"]}
    assert len(result["notation"]["nodes"]) == 2
    assert "error" not in result["notation"]


def test_projection_without_gaps_has_empty_gaps(test_store: Path):
    _create_sample_spec_and_nodes(test_store)
    assert evaluate_projection_view(test_store, {**VIEW, "nodes": [{"model": "SpecNodeDoc"}]})["gaps"] == []


def test_projection_strict_keeps_today_error(test_store: Path):
    _create_sample_spec_and_nodes(test_store)
    result = evaluate_projection_view(test_store, VIEW, strict=True)
    assert "no glyph of the notation matches SpecDoc:spec1" in result["notation"]["error"]


def test_resolve_documents_stays_strict(test_store: Path):
    _create_sample_spec_and_nodes(test_store)
    with pytest.raises(ViewError, match="no glyph of the notation matches"):
        resolve_documents(test_store, "NotationDoc:uml-class", [*NODES, GAP])
    res = resolve_documents(test_store, "NotationDoc:uml-class", [*NODES, GAP], strict=False)
    assert res["gaps"] == [{"id": GAP, "model": "SpecDoc"}] and len(res["nodes"]) == 2


def test_resolve_view_gaps_and_strict(test_store: Path, monkeypatch: pytest.MonkeyPatch):
    _create_sample_spec_and_nodes(test_store)
    assert resolve_view(test_store, "spec1")["gaps"] == []
    mod = sys.modules["sldb.api.notations.resolve_view"]
    original = mod.resolve_documents
    # the spec lists, besides its nodes, a document no glyph matches
    monkeypatch.setattr(mod, "resolve_documents", lambda store, ref, refs, **kw: original(store, ref, [*refs, GAP], **kw))
    loose = resolve_view(test_store, "spec1")
    assert loose["gaps"] == [{"id": GAP, "model": "SpecDoc"}] and len(loose["nodes"]) == 2
    with pytest.raises(ViewError, match="no glyph of the notation matches"):
        resolve_view(test_store, "spec1", strict=True)


def test_serve_returns_gaps_and_accepts_strict(test_store: Path):
    _create_sample_spec_and_nodes(test_store)
    server = ThreadingHTTPServer(("127.0.0.1", 0), build_handler(str(test_store), None, cors=False))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        status, data = _request_json(f"{base}/views/projection/evaluate", method="POST", data=VIEW)
        assert status == 200 and data["gaps"] == [{"id": GAP, "model": "SpecDoc"}]
        status, data = _request_json(f"{base}/views/projection/evaluate?strict=true", method="POST", data=VIEW)
        assert "error" in data["notation"]
        status, data = _request_json(f"{base}/notations/view?spec=spec1")
        assert data["gaps"] == []
    finally:
        server.shutdown()

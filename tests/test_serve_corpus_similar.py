"""GET /corpus/rank and GET /similar over a real served store."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from sldb.api import create_document
from tests.test_serve import _request_json, _stop
from tests.test_serve_edges_docs import _edge_store, _serve_at


def _corpus_store(tmp_path: Path):
    store, py = _edge_store(tmp_path)
    for name, title in (("pan", "Cocina del pan artesanal"), ("deploy", "Deploy del indice de campos")):
        create_document(store, "NoteDoc", tmp_path / f"{name}.md", {"title": title}, name=name, pythonpath=py)
    return _serve_at(store, py)


def _get(base: str, path: str, error: int | None = None):
    return _request_json(f"{base}{path}", expected_error=error)


def test_rank_without_index_is_an_explicit_409_not_an_empty_list(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        status, body = _get(base, "/corpus/rank?q=pan", 409)
        assert (status, body) == (409, {"ok": False, "error": "corpus no indexado", "kind": "not_indexed"})
        status, body = _get(base, "/corpus/rank?q=pan&fields=1", 409)
        assert status == 409 and body["kind"] == "not_indexed"
    finally:
        _stop(server, thread)


def test_rank_refresh_builds_the_index_then_plain_calls_read_it(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        status, body = _get(base, "/corpus/rank?q=cocina+del+pan&refresh=1&k=2")
        assert status == 200 and len(body["hits"]) == 2
        top = body["hits"][0]
        assert top["id"] == "NoteDoc:pan" and top["model"] == "NoteDoc" and top["name"] == "pan"
        assert set(top) == {"id", "model", "name", "score", "payload", "tags"} and top["payload"]["title"].startswith("Cocina")
        assert body["hits"][0]["score"] >= body["hits"][1]["score"]
        status, again = _get(base, "/corpus/rank?q=cocina+del+pan&k=1")
        assert status == 200 and again["hits"][0]["id"] == "NoteDoc:pan"
        _, none = _get(base, "/corpus/rank?q=cocina&threshold=2")
        assert none == {"hits": []}
    finally:
        _stop(server, thread)


def test_rank_among_and_fields(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        _, body = _get(base, "/corpus/rank?q=pan&refresh=1&among=NoteDoc:deploy,NoteDoc:n1")
        assert {hit["id"] for hit in body["hits"]} <= {"NoteDoc:deploy", "NoteDoc:n1"}
        _, fields = _get(base, "/corpus/rank?q=pan&fields=1&refresh=1&among=NoteDoc:pan&k=9")
        assert fields["hits"] and {hit["document_id"] for hit in fields["hits"]} == {"NoteDoc:pan"}
        assert set(fields["hits"][0]) == {"id", "document_id", "field", "model", "name", "score", "text", "payload", "tags"}
    finally:
        _stop(server, thread)


def test_rank_rejects_bad_parameters_with_400(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        assert _get(base, "/corpus/rank", 400) == (400, {"ok": False, "error": "Missing parameter: q"})
        status, body = _get(base, "/corpus/rank?q=x&k=abc", 400)
        assert status == 400 and "k" in body["error"]
        assert _get(base, "/corpus/rank?q=x&threshold=zz", 400)[0] == 400
    finally:
        _stop(server, thread)


def test_similar_lists_nodes_sharing_targets(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        status, body = _get(base, f"/similar?id={quote('NoteDoc:n1')}&types=ItemDoc")
        assert status == 200
        assert body == {"similar": [["sldb://document/ItemDoc:i1", 2]]}
        _, limited = _get(base, "/similar?id=NoteDoc:n1&limit=1")
        assert len(limited["similar"]) == 1
        _, by_node = _get(base, "/similar?id=sldb://document/NoteDoc:n1&relations=references")
        assert by_node == {"similar": []}
    finally:
        _stop(server, thread)


def test_similar_reports_missing_and_unknown_id(tmp_path: Path) -> None:
    server, thread, base = _corpus_store(tmp_path)
    try:
        assert _get(base, "/similar", 400) == (400, {"ok": False, "error": "Missing parameter: id"})
        status, body = _get(base, "/similar?id=NoteDoc:zzz", 404)
        assert status == 404 and body["ok"] is False and "NoteDoc:zzz" in body["error"]
        assert _get(base, "/similar?id=NoteDoc:n1&limit=0", 400)[0] == 400
    finally:
        _stop(server, thread)

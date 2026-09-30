"""GET /stores/check carries the model-vs-file divergence the CLI reports."""

from __future__ import annotations

from pathlib import Path

from tests.test_serve import _request_json, _stop
from tests.test_serve_edges_docs import _edge_store, _serve_at


def _check(base: str) -> dict:
    return _request_json(f"{base}/stores/check")[1]


def test_check_lists_every_model_and_document_when_clean(tmp_path: Path) -> None:
    store, py = _edge_store(tmp_path)
    server, thread, base = _serve_at(store, py)
    try:
        body = _check(base)
        assert body["ok"] is True and body["valid"] is True and body["checked"] >= 2 and body["mismatched"] == []
        assert body["root_ok"] is True and body["hash_a_ok"] is True and body["summary"]
        note = next(m for m in body["models"] if m["name"] == "NoteDoc")
        assert note["roster_ok"] and note["contract_ok"]
        doc = note["documents"][0]
        assert (doc["name"], doc["path"], doc["path_exists"], doc["note"]) == ("n1", "n1.md", True, "ok")
        assert doc["content_ok"] and doc["fields_ok"] and doc["hash_c_ok"] and doc["hash_d_ok"]
    finally:
        _stop(server, thread)


def test_check_reports_file_divergence_and_missing_file(tmp_path: Path) -> None:
    store, py = _edge_store(tmp_path)
    (tmp_path / "n1.md").write_text("# Editado a mano\n", encoding="utf-8")
    (tmp_path / "i1.md").unlink()
    server, thread, base = _serve_at(store, py)
    try:
        body = _check(base)
        assert body["ok"] is False and body["valid"] is False
        docs = {d["name"]: d for m in body["models"] for d in m["documents"]}
        assert docs["n1"]["path_exists"] is True and docs["n1"]["content_ok"] is False and docs["n1"]["note"] != "ok"
        assert docs["i1"]["path_exists"] is False and docs["i1"]["explain"]
        assert {"damaged", "reformatted", "roster_only", "moved_contracts", "mismatched"} <= set(body)
    finally:
        _stop(server, thread)

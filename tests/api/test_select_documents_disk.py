"""The candidate rows of `select_documents` kept on disk (H11b): the same rows with and without
the file, a written or tracked document read at the next call, a corrupt or foreign file ignored."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api import select_documents, track_document_file
from tests.api.test_select_documents import store  # noqa: F401  (the fixture)
from tests.api.test_views import world  # noqa: F401  (the fixture)


def _file(store_path: Path) -> Path:
    found = list((store_path.parent / ".sldb_cache" / "document_rows").glob("*.json"))
    assert len(found) == 1
    return found[0]


def _rows(store_path: Path) -> list[dict]:
    return select_documents(store_path, {"include_linked": True})


def test_the_rows_are_the_same_with_and_without_the_file(store: Path) -> None:
    first = _rows(store)
    saved = _file(store)
    assert _rows(store) == first
    saved.unlink()
    assert _rows(store) == first
    assert _file(store).is_file()


def test_the_view_style_selection_reads_the_file_not_the_shards(store: Path, monkeypatch) -> None:
    first = _rows(store)
    from sldb.store.query_engine import document_selection

    monkeypatch.setattr(document_selection, "store_rows", lambda *a, **k: (_ for _ in ()).throw(AssertionError("shards read")))
    assert _rows(store) == first


def test_a_tracked_document_is_seen_by_the_next_call(store: Path) -> None:
    before = _rows(store)
    root = store.parent
    (root / "later.md").write_text((root / "task-a.md").read_text(encoding="utf-8"), encoding="utf-8")
    track_document_file(store, "BaseDoc", root / "later.md", "later", str(root.parent))
    after = _rows(store)
    assert len(after) == len(before) + 1
    assert "BaseDoc:later" in [row["export_id"] for row in after]


def test_a_corrupt_or_foreign_file_is_ignored_without_error(store: Path) -> None:
    first = _rows(store)
    saved = _file(store)
    for text in ("{not json", "[]", json.dumps({"key": {}, "rows": "x"}), json.dumps({"key": 1})):
        saved.write_text(text, encoding="utf-8")
        assert _rows(store) == first
        assert len(json.loads(saved.read_text(encoding="utf-8"))["rows"]) == len(first)


def test_another_format_is_a_miss(store: Path) -> None:
    first = _rows(store)
    saved = _file(store)
    data = json.loads(saved.read_text(encoding="utf-8"))
    data["key"]["format"] = "0"
    data["rows"] = []
    saved.write_text(json.dumps(data), encoding="utf-8")
    assert _rows(store) == first


def test_a_view_gives_the_same_result_and_revision_with_and_without_the_file(world) -> None:  # noqa: F811
    from sldb import api

    first = api.run_view(world.store, "tablero")
    rows_dir = world.store.parent / ".sldb_cache" / "document_rows"
    assert list(rows_dir.glob("*.json"))
    assert api.run_view(world.store, "tablero") == first
    for saved in rows_dir.glob("*.json"):
        saved.unlink()
    assert api.run_view(world.store, "tablero") == first
    world.save("Item", "i4", {"title": "I4", "status": "open", "owner": "ana", "stage": "Stage:open", "depends_on": []})
    assert api.run_view(world.store, "tablero")["revision"] != first["revision"]

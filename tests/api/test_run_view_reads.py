"""H11: `run_view` composes the edge index of the calling store alone unless the view can name a
linked store, and a composed index survives the process in the store's `.sldb_cache`."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.edge_index import compose
from sldb.store.edge_index.compose import invalidate_composed_edge_indexes
from sldb.store.io.shards import invalidate_shard_cache

MODULE = "sldb_h11_run_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


def view(name: str, select: dict) -> dict:
    return {"id": name, "name": name, "title": name, "sections": [{"key": "notes", "select": select, "fields": ["title"]}]}


def make_store(base: Path, name: str, py: str) -> tuple[Path, Path]:
    root = base / name
    root.mkdir()
    store = api.init_store(root).store_path
    for ref in (f"{MODULE}:Note", "sldb.models.notation_models:ViewDoc"):
        api.add_model(store, ref, py)
    return root, store


def note(root: Path, store: Path, py: str, name: str, title: str) -> None:
    api.create_document(store, "Note", root / f"{name}.md", {"title": title}, name, py)


@pytest.fixture
def linked(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        py = str(tmp_path)
        (a_root, a), (b_root, b) = make_store(tmp_path, "A", py), make_store(tmp_path, "B", py)
        note(a_root, a, py, "a1", "from A")
        note(b_root, b, py, "b1", "from B")
        for name, select in (("local", {"model": "Note"}), ("wide", {"model": "Note", "include_linked": True}), ("byref", {"prefix": "B:b"})):
            api.create_document(a, "ViewDoc", a_root / f"{name}.md", view(name, select), name, py)
        api.link_store(a, b, name="B")
        yield a, lambda title: note(b_root, b, py, "b2", title)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def reads(monkeypatch, name: str, store: Path) -> tuple[list[bool], dict]:
    seen: list[bool] = []
    run = sys.modules["sldb.api.views.view_reading"]
    original = run.load_edge_index
    monkeypatch.setattr(run, "load_edge_index", lambda s, include_linked=True, **k: seen.append(include_linked) or original(s, include_linked=include_linked, **k))
    return seen, api.run_view(store, name)


def test_a_view_that_names_no_link_reads_only_the_calling_store(linked, monkeypatch) -> None:
    a, _ = linked
    seen, result = reads(monkeypatch, "local", a)
    assert seen == [False]
    assert [r["export_id"] for r in result["sections"]["notes"]["rows"]] == ["Note:a1"]


@pytest.mark.parametrize("name", ["wide", "byref"])
def test_a_view_that_can_name_a_link_reads_the_linked_stores(linked, monkeypatch, name: str) -> None:
    a, _ = linked
    seen, _ = reads(monkeypatch, name, a)
    assert seen == [False, True]


def test_the_revision_follows_a_linked_store_only_for_a_view_that_selects_it(linked) -> None:
    a, add_b_note = linked
    before = {n: api.run_view(a, n)["revision"] for n in ("local", "wide")}
    add_b_note("new in B")
    after = {n: api.run_view(a, n) for n in ("local", "wide")}
    assert after["local"]["revision"] == before["local"]
    assert after["wide"]["revision"] != before["wide"]
    assert "B:Note:b2" in [r["export_id"] for r in after["wide"]["sections"]["notes"]["rows"]]


def forget_process() -> None:
    invalidate_composed_edge_indexes()
    invalidate_shard_cache()


def test_a_new_process_reads_the_composed_index_from_disk_and_a_moved_store_recomposes(linked, monkeypatch) -> None:
    a, add_b_note = linked
    first = api.run_view(a, "local")
    composed = []
    original = compose._compose
    monkeypatch.setattr(compose, "_compose", lambda *args: composed.append(1) or original(*args))
    forget_process()
    assert api.run_view(a, "local") == first and composed == []
    add_b_note("moves B")
    forget_process()
    api.run_view(a, "wide")
    api.run_view(a, "wide")
    forget_process()
    assert api.run_view(a, "wide")["sections"] and len(composed) == 1

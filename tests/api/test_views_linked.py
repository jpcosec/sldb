"""H9: a ViewDoc tracked by a linked store (DA4: deskops' views ship only in its package store).

Store A links to B; the view `board` lives only in B. `run_view(A, "board")` finds it, reads
its file from B's root (through the read guard) and evaluates it over A's documents."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.core.exceptions import SLDBDocumentTargetError

MODULE = "sldb_h9_linked_view_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


def board(key: str, title: str = "Board") -> dict:
    return {"id": "board", "name": "board", "title": title, "sections": [{"key": key, "select": {"model": "Note"}, "fields": ["title"]}]}


class Store:
    def __init__(self, base: Path, name: str, py: str) -> None:
        self.root, self.py = base / name, py
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for ref in (f"{MODULE}:Note", "sldb.models.notation_models:ViewDoc"):
            api.add_model(self.store, ref, py)

    def doc(self, model: str, name: str, payload: dict) -> Path:
        path = self.root / model.lower() / f"{name}.md"
        api.create_document(self.store, model, path, payload, name, self.py)
        return path

    def link(self, other: "Store", name: str) -> None:
        api.link_store(self.store, other.store, name=name)


@pytest.fixture
def stores(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        a, b = Store(tmp_path, "A", str(tmp_path)), Store(tmp_path, "B", str(tmp_path))
        a.doc("Note", "a1", {"title": "from A"})
        b.doc("Note", "b1", {"title": "from B"})
        b.doc("ViewDoc", "board", board("notes"))
        a.link(b, "B")
        yield a, b
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_view_only_in_the_linked_store_is_found_and_evaluated_over_the_calling_store(stores) -> None:
    a, _ = stores
    (a.root / "viewdoc").mkdir()
    (a.root / "viewdoc" / "board.md").write_text("# not the view: B's root is read, not A's\n", encoding="utf-8")
    result = api.run_view(a.store, "board")
    assert result["view"] == "board"
    assert [(r["export_id"], r["fields"]) for r in result["sections"]["notes"]["rows"]] == [("Note:a1", {"title": "from A"})]
    assert api.run_view(a.store, "B:board")["revision"] == result["revision"]


def test_list_views_lists_the_linked_view(stores) -> None:
    a, _ = stores
    assert api.list_views(a.store) == [{"name": "board", "title": "Board", "params": [], "sections": ["notes"]}]


def test_two_linked_views_with_one_name_are_ambiguous_and_listed_qualified(stores, tmp_path: Path) -> None:
    a, _ = stores
    c = Store(tmp_path, "C", str(tmp_path))
    c.doc("ViewDoc", "board", board("other"))
    a.link(c, "C")
    with pytest.raises(SLDBDocumentTargetError) as caught:
        api.run_view(a.store, "board")
    assert str(caught.value) == "Ambiguous view: board (linked in B, C)"
    assert [v["name"] for v in api.list_views(a.store)] == ["B:board", "C:board"]
    assert list(api.run_view(a.store, "C:board")["sections"]) == ["other"]


def test_a_local_view_wins_over_a_linked_one(stores) -> None:
    a, _ = stores
    a.doc("ViewDoc", "board", board("mine", "Mine"))
    assert list(api.run_view(a.store, "board")["sections"]) == ["mine"]
    assert list(api.run_view(a.store, "B:board")["sections"]) == ["notes"]
    assert [(v["name"], v["title"]) for v in api.list_views(a.store)] == [("B:board", "Board"), ("board", "Mine")]


def test_the_revision_moves_when_the_linked_view_changes(stores) -> None:
    a, b = stores
    before = api.run_view(a.store, "board")["revision"]
    api.save_document_payload(b.store, "ViewDoc", "board", board("notes", "Board v2"), b.py)
    assert api.run_view(a.store, "board")["revision"] != before


def test_a_linked_view_file_swapped_for_a_symlink_out_of_its_root_is_not_read(stores, tmp_path: Path) -> None:
    a, b = stores
    path = b.root / "viewdoc" / "board.md"
    outside = tmp_path / "outside.md"
    outside.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(outside)
    with pytest.raises(SLDBDocumentTargetError, match="outside-root"):
        api.run_view(a.store, "board")

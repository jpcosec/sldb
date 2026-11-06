"""A bare id in a field that allows a model also names a document of one of its submodels.

An instance of a submodel is an instance of its bases. A field that allows `Note` and holds
`m1` names `Memo:m1` when `Memo(Note)` tracks it, as deskops' `depends_on` (allows `TaskDoc`)
names a task tracked as `TaskCodeDoc`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api

MODULE = "sldb_declared_ref_family_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Memo(Note):
    pass


class Letter(Note):
    pass


class Linked(StructuredNLDoc):
    __references__ = ["about"]
    __reference_models__ = {"about": ["Note"]}
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(default="", description="Referenced note id.")
'''


class World:
    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Note", "Memo", "Letter", "Linked"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{model}-{name}.md", payload, name, self.py)

    def about(self, name: str, value: str) -> list:
        self.create("Linked", name, {"title": name, "about": value})
        api.rebuild_edges(self.store, self.py)
        return [e.target for e in api.edges_from(self.store, f"Linked:{name}", "references")]


@pytest.fixture
def world(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_bare_id_names_the_document_of_a_submodel(world: World) -> None:
    world.create("Memo", "m1", {"title": "m1"})
    assert world.about("l1", "m1") == ["sldb://document/Memo:m1"]


def test_the_allowed_model_itself_wins_over_a_submodel(world: World) -> None:
    world.create("Note", "same", {"title": "same"})
    world.create("Memo", "same", {"title": "same"})
    assert world.about("l1", "same") == ["sldb://document/Note:same"]


def test_two_submodels_with_that_name_are_ambiguous_and_no_edge(world: World) -> None:
    world.create("Memo", "twin", {"title": "twin"})
    world.create("Letter", "twin", {"title": "twin"})
    assert world.about("l1", "twin") == []
    reasons = [u.reason for u in api.unresolved_references(world.store) if u.target == "twin"]
    assert reasons == ["ambiguous"]


def test_inherited_models_resolve_through_the_bases_of_their_classes(tmp_path: Path) -> None:
    """A repo inherits the models from the store that owns them (as desks inherit deskops'):
    its local model indexes keep no `base_models`, and the reference still names the submodel."""
    owner, local = tmp_path / "owner", tmp_path / "repo"
    owner.mkdir(), local.mkdir()
    (owner / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(owner))
    try:
        owner_sp, local_sp = api.init_store(owner).store_path, api.init_store(local).store_path
        for model in ("Note", "Memo", "Linked"):
            api.add_model(owner_sp, f"{MODULE}:{model}", str(owner))
        api.link_store(local_sp, owner_sp, "owner")
        for model in ("Note", "Memo", "Linked"):
            api.inherit_model(local_sp, f"owner:{model}")
        api.create_document(local_sp, "Memo", local / "m.md", {"title": "m1"}, "m1")
        api.create_document(local_sp, "Linked", local / "l.md", {"title": "l1", "about": "m1"}, "l1")
        api.rebuild_edges(local_sp)
        assert [e.target for e in api.edges_from(local_sp, "Linked:l1", "references")] == ["sldb://document/Memo:m1"]
    finally:
        sys.path.remove(str(owner))
        sys.modules.pop(MODULE, None)

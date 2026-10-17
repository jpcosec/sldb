"""Declared reference fields reach the edge index.

A model that declares `__references__` or `__containment__` says that a field holds the id of
another document. Everything else a model declares already becomes an edge -- `model_fields`
becomes `has_field`, `base_models` becomes `extends`, `__semantics__` becomes `tagged_as` --
and these two were readable metadata only.

Covers: both dunders produce edges carrying the field name; a list field produces one edge per
id; a target that is not tracked is dropped rather than reported, because the model declared a
shape and not an authored assertion; a relation document is left to its own contribution
instead of asserting its ends twice.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api

MODULE = "sldb_declared_ref_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "note"]}
    __template__ = "# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    title: str = Field(description="Title.")
    body: str = Field(default="", description="Body.")


class Linked(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "linked"]}
    __references__ = ["about"]
    __containment__ = {"steps": ["Note"]}
    __template__ = "---\\nabout: ⸢rev•about⸥\\nsteps: ⸢rev,list•steps⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(default="", description="Referenced document export id.")
    steps: list = Field(default_factory=list, description="Contained document export ids.")
'''


class World:
    """A store with a referencing model registered and two notes to point at."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Note", "Linked"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)
        for name in ("n1", "n2"):
            self.create("Note", name, {"title": name, "body": "text"})

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def link(self, name: str, about: str = "", steps: list | None = None) -> None:
        self.create("Linked", name, {"title": name, "about": about, "steps": steps or []})

    def edges_of(self, name: str, relation: str | None = None) -> list:
        api.rebuild_edges(self.store, self.py)
        return api.edges_from(self.store, f"Linked:{name}", relation)


@pytest.fixture
def world(tmp_path: Path) -> World:
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield World(tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def _pairs(edges) -> set:
    return {(e.target, e.relation, e.metadata.get("field")) for e in edges}


def test_a_declared_reference_becomes_an_edge_that_names_its_field(world: World) -> None:
    world.link("l1", about="Note:n1")
    assert ("sldb://document/Note:n1", "references", "about") in _pairs(world.edges_of("l1"))


def test_a_containment_field_becomes_contains_and_carries_the_models_it_allows(world: World) -> None:
    world.link("l1", steps=["Note:n1"])
    edge = next(e for e in world.edges_of("l1", "contains"))
    assert edge.target == "sldb://document/Note:n1"
    assert edge.metadata["allowed_models"] == ["Note"]


def test_a_list_field_produces_one_edge_per_id(world: World) -> None:
    world.link("l1", steps=["Note:n1", "Note:n2"])
    assert len(world.edges_of("l1", "contains")) == 2


def test_a_reference_to_an_untracked_document_is_dropped_not_reported(world: World) -> None:
    world.link("l1", about="Note:missing")
    assert world.edges_of("l1", "references") == []
    assert api.check_edges(world.store).ok


def test_a_bare_name_without_its_model_is_not_guessed_at(world: World) -> None:
    world.link("l1", about="n1")
    assert world.edges_of("l1", "references") == []


def test_a_relation_document_does_not_assert_its_own_ends_twice(world: World) -> None:
    """`RelationDoc.__references__` names the ends of the edge it already contributes."""
    world.create("RelationTypeDoc", "rt-x", {"title": "x", "name": "x", "direction": "directed", "cardinality": "many_to_many", "axis": "WHAT", "source_types": [], "target_types": [], "condition": "", "description": "x."})
    world.create("RelationDoc", "r1", {"title": "r1", "source_id": "Note:n1", "target_id": "Note:n2", "relation_type": "x", "condition": "", "notes": ""})
    api.rebuild_edges(world.store, world.py)
    assert api.edges_from(world.store, "RelationDoc:r1", "references") == []
    assert api.check_edges(world.store).ok


def test_a_reference_to_a_relation_type_document_reaches_its_relation_type_node(world: World) -> None:
    """A RelationTypeDoc is indexed as a `relation_type` node, not a document node; a reference
    written as its export id used to dangle and be dropped while `doc_exists` said it was there."""
    world.create("RelationTypeDoc", "rt-x", {"title": "x", "name": "x", "direction": "directed", "cardinality": "many_to_many", "axis": "WHAT", "source_types": [], "target_types": [], "condition": "", "description": "x."})
    world.link("l1", about="RelationTypeDoc:rt-x")
    assert ("sldb://relation_type/x", "references", "about") in _pairs(world.edges_of("l1"))
    assert api.check_edges(world.store).ok

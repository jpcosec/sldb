"""A composed field reaches the graph, so impact radius can follow the recursion.

`__compositions__` renders another document's payload into this one's text. That ref was the one
declaration naming another document that produced no edge: changing a child left nothing saying
which composed parent went stale. Now it contributes `composes`, carrying which field composed
it and the ref as authored.

A ref is a project path, not an export id, so the target is resolved when the index is composed
(which document owns a path is not something one shard can know). Covers: the edge and its
metadata, the reverse lookup that impact radius needs, path forms that mean the same document,
a ref no document owns, a composed field declaring no source field, and `edges check` accepting
the relation type.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api

MODULE = "sldb_composition_edge_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "task"]}
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")


class Board(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "board"]}
    __compositions__ = {
        "task_summaries": {
            "source_field": "tasks",
            "model": "%s:Task",
            "template": "- {title} [{status}]",
        }
    }
    __template__ = "# ⸢rev•title⸥\\n\\n## Tasks\\n\\n- ⸢rev,list•tasks⸥\\n\\n## Summary\\n\\n⸢render•task_summaries⸥"
    title: str = Field(description="Title.")
    tasks: list[str] = Field(default_factory=list, description="Task refs, project-relative.")


class Sourceless(StructuredNLDoc):
    __compositions__ = {"summary": {"model": "%s:Task", "template": "- {title}"}}
    __template__ = "# ⸢rev•title⸥\\n\\n## Summary\\n\\n⸢render•summary⸥"
    title: str = Field(description="Title.")
''' % (MODULE, MODULE)


class World:
    """A store with a Task tracked at `sub/task-a.md` and models able to compose it."""

    def __init__(self, base: Path) -> None:
        sys.modules.pop(MODULE, None)
        (base / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
        self.root, self.py = base / "project", str(base)
        self.root.mkdir()
        (self.root / "sub").mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Task", "Board", "Sourceless"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)
        api.create_document(self.store, "Task", self.root / "sub" / "task-a.md", {"title": "Ship it", "status": "active"}, "task-a", self.py)

    def board(self, tasks: list[str], name: str = "board") -> None:
        api.create_document(self.store, "Board", self.root / f"{name}.md", {"title": name, "tasks": tasks}, name, self.py)

    def composes(self, name: str = "board") -> list:
        return api.edges_from(self.store, f"Board:{name}", "composes")


@pytest.fixture
def world(tmp_path: Path) -> World:
    return World(tmp_path)


def test_a_composed_field_contributes_a_composes_edge(world: World):
    world.board(["sub/task-a.md"])

    edges = world.composes()

    assert [e.target for e in edges] == ["sldb://document/Task:task-a"]


def test_the_edge_carries_the_field_and_the_ref_as_authored(world: World):
    world.board(["sub/task-a.md"])

    metadata = world.composes()[0].metadata

    assert metadata["field"] == "task_summaries"
    assert metadata["source_field"] == "tasks"
    assert metadata["ref_path"] == "sub/task-a.md"
    assert metadata["composed_model"] == "Task"
    assert metadata["origin"] == "schema"


def test_impact_radius_finds_the_parents_that_compose_a_document(world: World):
    world.board(["sub/task-a.md"], "board-one")
    world.board(["sub/task-a.md"], "board-two")

    composing = api.edges_to(world.store, "Task:task-a", "composes")

    assert sorted(e.source for e in composing) == ["sldb://document/Board:board-one", "sldb://document/Board:board-two"]


def test_a_ref_written_differently_resolves_to_the_same_document(world: World):
    world.board(["./sub/task-a.md"])

    assert [e.target for e in world.composes()] == ["sldb://document/Task:task-a"]


def test_a_ref_no_document_owns_keeps_no_edge(world: World):
    world.board(["sub/task-a.md", "nowhere.md"])

    assert [e.metadata["ref_path"] for e in world.composes()] == ["sub/task-a.md"]


def test_a_composed_field_without_a_source_field_contributes_nothing(world: World):
    api.create_document(world.store, "Sourceless", world.root / "lonely.md", {"title": "Lonely"}, "lonely", world.py)

    assert api.edges_from(world.store, "Sourceless:lonely", "composes") == []


def test_edges_check_accepts_the_composes_relation(world: World):
    world.board(["sub/task-a.md"])

    assert api.check_edges(world.store, str(world.root)).errors == []

"""A composed field resolves its refs against the project root on every write path.

`compose_field` takes a `ref_root` precisely because resolving a ref against the working
directory made the same document compose differently depending on where the caller ran — and a
ref that does not resolve renders as empty text, so the loss is silent. `sldb render` passed the
root, but the write paths (`create_document`, `save_document_payload`, `docs update`) and the
segment views did not: a document created from one directory and re-saved from another lost its
composed summary without a word.
"""

from __future__ import annotations

import sys
from pathlib import Path

from sldb import api

MODULE = "sldb_compose_root_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Task(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")


class Board(StructuredNLDoc):
    __compositions__ = {
        "summary": {
            "source_field": "tasks",
            "model": "%s:Task",
            "template": "- {title} [{status}]",
        }
    }
    __template__ = "# ⸢rev•title⸥\\n\\n## Tasks\\n\\n- ⸢rev,list•tasks⸥\\n\\n## Summary\\n\\n⸢render•summary⸥"
    title: str = Field(description="Title.")
    tasks: list[str] = Field(default_factory=list, description="Task refs, project-relative.")
''' % MODULE

SUMMARY = "- Ship the CLI [active]"


class World:
    """A store with a Board whose composed summary reads a Task tracked beside it."""

    def __init__(self, base: Path) -> None:
        sys.modules.pop(MODULE, None)
        (base / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
        self.root, self.py = base / "project", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Task", "Board"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.create_document(self.store, "Task", self.root / "task-a.md", {"title": "Ship the CLI", "status": "active"}, "task-a", self.py)

    def board(self, payload: dict) -> Path:
        return api.create_document(self.store, "Board", self.root / "board.md", payload, "board", self.py).path


def _elsewhere(tmp_path: Path, monkeypatch) -> None:
    """Run from a directory that is not the project root, as any real caller may."""
    other = tmp_path / "elsewhere"
    other.mkdir()
    monkeypatch.chdir(other)


def test_create_document_composes_against_the_project_root(tmp_path: Path, monkeypatch):
    world = World(tmp_path)
    _elsewhere(tmp_path, monkeypatch)

    path = world.board({"title": "Board", "tasks": ["task-a.md"]})

    assert SUMMARY in path.read_text(encoding="utf-8")


def test_save_document_payload_composes_against_the_project_root(tmp_path: Path, monkeypatch):
    world = World(tmp_path)
    path = world.board({"title": "Board", "tasks": ["task-a.md"]})
    _elsewhere(tmp_path, monkeypatch)

    api.save_document_payload(world.store, "Board", "board", {"title": "Renamed", "tasks": ["task-a.md"]}, world.py)

    text = path.read_text(encoding="utf-8")
    assert "# Renamed" in text and SUMMARY in text


def test_document_segments_compose_against_the_project_root(tmp_path: Path, monkeypatch):
    world = World(tmp_path)
    world.board({"title": "Board", "tasks": ["task-a.md"]})
    _elsewhere(tmp_path, monkeypatch)

    segments = api.build_document_segments(world.store, world.py, "Board/board")

    assert SUMMARY in segments.text
    assert segments.canonical is True

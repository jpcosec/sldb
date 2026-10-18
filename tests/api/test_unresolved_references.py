"""A declared reference names its document by export id, by path, or by a bare id the field's
models qualify; what names nothing is reported, never stored as an edge.

deskops writes `depends_on: [task-x]` and `pills: [desk/contexts/pill-x.md]`. Only
`Model:name` used to count, so none of those reached the edge index, and a qualified id to a
missing document was dropped without a trace (the deskops F4 request).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api

MODULE = "sldb_unresolved_ref_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Pill(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Task(StructuredNLDoc):
    __references__ = ["depends_on", "about"]
    __reference_models__ = {"depends_on": ["Task"], "either": ["Task", "Pill"]}
    __containment__ = {"pills": ["Pill"]}
    __template__ = "---\\ndepends_on: ⸢rev,list•depends_on⸥\\nabout: ⸢rev,list•about⸥\\neither: ⸢rev,list•either⸥\\npills: ⸢rev,list•pills⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    depends_on: list = Field(default_factory=list, description="Tasks this one waits for.")
    about: list = Field(default_factory=list, description="Free references: files, commits, ids.")
    either: list = Field(default_factory=list, description="A task or a pill.")
    pills: list = Field(default_factory=list, description="Contained pills.")
'''


@pytest.fixture
def store(tmp_path: Path):
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    added = str(tmp_path)
    root, py = tmp_path / "world", str(tmp_path)
    root.mkdir()
    sp = api.init_store(root).store_path
    for model in ("Pill", "Task"):
        api.add_model(sp, f"{MODULE}:{model}", py)
    (root / "pills").mkdir()

    def create(model: str, path: str, name: str, payload: dict) -> None:
        api.create_document(sp, model, root / path, {"title": name, **payload}, name, py)

    create("Pill", "pills/p1.md", "p1", {})
    create("Pill", "pills/dup.md", "dup", {})
    create("Task", "dup.md", "dup", {})
    create("Task", "b.md", "b", {})
    create("Task", "a.md", "a", {
        "depends_on": ["b", "nope", "Task:gone"],
        "about": ["3900ad4", "docs/untracked.md", "https://example.org/x", "b.md"],
        "either": ["dup"],
        "pills": ["pills/p1.md", "./pills/ghost.md"],
    })
    api.rebuild_edges(sp, py)
    try:
        yield sp
    finally:
        if added in sys.path:
            sys.path.remove(added)
        sys.modules.pop(MODULE, None)


def _targets(sp, relation: str) -> list[str]:
    return sorted(e.target for e in api.edges_from(sp, "Task:a", relation) if "field" in e.metadata)


def test_a_bare_id_and_a_path_reach_their_documents(store):
    assert _targets(store, "references") == ["sldb://document/Task:b", "sldb://document/Task:b"]  # depends_on b, about b.md
    assert _targets(store, "contains") == ["sldb://document/Pill:p1"]


def test_what_names_no_document_is_reported_with_why(store):
    found = {(r.field, r.target): r for r in api.unresolved_references(store)}
    assert set(found) == {("depends_on", "nope"), ("depends_on", "Task:gone"), ("either", "dup"), ("pills", "./pills/ghost.md")}
    assert (found[("depends_on", "nope")].reason, found[("depends_on", "nope")].target_export_id) == ("missing_document", "Task:nope")
    assert found[("depends_on", "Task:gone")].reason == "missing_document"
    assert found[("either", "dup")].reason == "ambiguous"
    ghost = found[("pills", "./pills/ghost.md")]
    assert (ghost.reason, ghost.relation, ghost.source, ghost.model, ghost.source_path) == ("unknown_path", "contains", "Task:a", "Task", "a.md")


def test_a_free_field_reports_nothing_unqualified(store):
    """`about` declares no models: a commit, an untracked file or a URL is not a document."""
    assert not [r for r in api.unresolved_references(store) if r.field == "about"]


def test_tracking_the_missing_document_resolves_it_without_touching_the_source(store, tmp_path):
    root = tmp_path / "world"
    api.create_document(store, "Task", root / "nope.md", {"title": "nope"}, "nope", str(tmp_path))
    api.rebuild_edges(store, str(tmp_path))
    assert "sldb://document/Task:nope" in _targets(store, "references")
    assert ("depends_on", "nope") not in {(r.field, r.target) for r in api.unresolved_references(store)}


def test_the_cli_lists_them(store, capsys):
    from sldb.cli import main

    assert main(["edges", "unresolved", "--store", str(store)]) == 0
    assert "4 unresolved reference(s)" in capsys.readouterr().out


def test_only_a_model_that_declares_reference_models_moves_its_contract():
    from pydantic import Field

    from sldb.api import StructuredNLDoc
    from sldb.store.hashing import _core_contract_parts, hash_model_contract, hash_payload

    class Plain(StructuredNLDoc):
        __references__ = ["about"]
        __template__ = "# ⸢rev•title⸥"
        title: str = Field(description="Title.")

    class Declaring(Plain):
        __reference_models__ = {"about": ["Plain"]}

    assert hash_model_contract(Plain) == hash_payload(_core_contract_parts(Plain)), "no store's contract moves"
    assert hash_model_contract(Declaring) != hash_payload(_core_contract_parts(Declaring))

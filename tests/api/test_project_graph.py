"""A project's declared-edge graph: nodes from its files, edges from its store index and its texts.

The project (deskops' desk is the first) only configures where documents live, which files
are nodes and which fields and sections declare references; `ProjectGraph` reads the rest.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.edges.project_graph import (
    DeclaredFileTargets, DocumentSurface, FileExclusions, FileRule, LineMentions, MentionPattern,
    MissingTargetKind, ProjectGraph, ProjectGraphConfig, ReferenceField, SectionMentions,
    extract_document_nodes, extract_file_nodes,
)
from sldb.api.stores.tracked_documents import tracked_documents

MODULE = "sldb_project_graph_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Card(StructuredNLDoc):
    __references__ = ["depends_on"]
    __reference_models__ = {"depends_on": ["Card"]}
    __containment__ = {"notes": ["Note"]}
    __template__ = "---\\nid: ⸢rev•id⸥\\ndepends_on: ⸢rev,list•depends_on⸥\\nnotes: ⸢rev,list•notes⸥\\n---\\n\\n# ⸢rev•title⸥"
    id: str = Field(description="Card id.")
    title: str = Field(description="Title.")
    depends_on: list = Field(default_factory=list, description="Cards this one waits for.")
    notes: list = Field(default_factory=list, description="Contained notes.")
'''

PATH = MentionPattern(regex=r"(?<![\w/.-])(?P<path>src/[A-Za-z0-9_./-]+\.py)", target="{path}")
CONFIG = ProjectGraphConfig(
    document_extractor="docs_v1", file_extractor="files_v1", edge_extractor="edges_v1",
    surfaces=(
        DocumentSurface(kind="card", directory="cards", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
        DocumentSurface(kind="note", directory="notes", pattern="*.md"),
        DocumentSurface(kind="issue", directory="issues", pattern="*.md", identity="document_id_or_slug"),
    ),
    file_rules=(
        FileRule(kind="test_file", file_kind="test", path_prefixes=("tests",), suffixes=(".py",)),
        FileRule(kind="source_file", file_kind="source", path_prefixes=("src",), suffixes=(".py",)),
    ),
    exclusions=FileExclusions(directories=("build",), path_prefixes=("src/vendored",)),
    declared_file_targets=(DeclaredFileTargets(directory="cards", field="target", kind="source_file", file_kind="source", source_kind="declared_target"),),
    reference_fields=(ReferenceField(path=("topics",), target_prefix="topic:", default_role="mentions", allowed_roles=("mentions", "defines")),),
    fields_by_kind={"card": ("depends_on", "notes")},
    fields_by_model={"Card": ("notes", "depends_on")},
    kind_by_model={"Card": "card"},
    section_mentions=(SectionMentions(headings=("related cards",), patterns=(MentionPattern(regex=r"\bcard-[a-z0-9-]+\b", target="card:{0}"),), role="relates"),),
    line_mentions=(LineMentions(kinds=("card",), patterns=(PATH,), role="touches", locator="path"),),
    missing_target_kinds=(MissingTargetKind(parts=("src",), ending=".py", kind="source_file"),),
    closed_document=lambda kind, text: kind == "issue" and "Status: closed" in text,
)


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    _write(root / "cards" / "card-a.md", "---\nid: card-a\ntopics:\n  - auth\n  - {id: login, role: defines}\ntarget: generated/out.py\n---\n\n# Card A\n\nTouches src/app.py and src/gone.py.\n\n## Related cards\n\n- card-b\n- card-zz\n\n```yaml\ntopics: [yaml-topic]\n```\n")
    _write(root / "cards" / "card-b.md", "---\nid: card-b\nrecord: true\n---\n\n# Card B\n\nsrc/app.py\n")
    _write(root / "cards" / "Board.md", "# Board\n")
    _write(root / "notes" / "n1.md", "# First note\n")
    _write(root / "issues" / "broken-login.md", "# Broken Login\n\nStatus: closed\n\n## Related cards\n\n- card-a\n")
    _write(root / "src" / "app.py", "")
    _write(root / "src" / "vendored" / "lib.py", "")
    _write(root / "build" / "src" / "x.py", "")
    _write(root / "tests" / "test_app.py", "")
    _write(root / "generated" / "out.py", "")
    return root


def test_nodes_follow_the_surfaces_and_the_file_rules(project: Path) -> None:
    documents = {node.id: node for node in extract_document_nodes(project, CONFIG)}
    assert set(documents) == {"card:card-a", "card:card-b", "note:notes/n1.md", "issue:broken-login"}
    assert documents["note:notes/n1.md"].label == "First note"
    assert documents["card:card-a"].provenance.extractor == "docs_v1"
    files = {node.id: node.provenance.source_kind for node in extract_file_nodes(project, CONFIG)}
    assert files == {"source_file:src/app.py": "path_rule", "test_file:tests/test_app.py": "path_rule", "source_file:generated/out.py": "declared_target"}


def test_declarations_resolve_to_edges_or_missing_targets(project: Path) -> None:
    graph = ProjectGraph(project, CONFIG)
    edges = {(e.source_id, e.target_id, e.role, e.provenance_locator, e.record) for e in graph.extraction().edges}
    assert ("card:card-a", "source_file:src/app.py", "touches", "line:11:path", None) in edges
    assert ("card:card-a", "card:card-b", "relates", "line:15:related cards", None) in edges
    assert ("card:card-b", "source_file:src/app.py", "touches", "line:8:path", True) in edges
    assert ("issue:broken-login", "card:card-a", "relates", "line:7:related cards", True) in edges
    missing = {(m.source_id, m.target_id, m.provenance_locator) for m in graph.extraction().missing_targets}
    assert missing == {
        ("card:card-a", "topic:auth", "frontmatter"), ("card:card-a", "topic:login", "frontmatter"),
        ("card:card-a", "source_file:src/gone.py", "line:11:path"), ("card:card-a", "card:card-zz", "line:16:related cards"),
        ("card:card-a", "topic:yaml-topic", "line:18:yaml"),
    }


def test_one_source_read_alone_is_its_part_of_the_whole(project: Path) -> None:
    whole = ProjectGraph(project, CONFIG).extraction()
    alone = ProjectGraph(project, CONFIG)
    assert alone.edges_from("card:card-a") == [e for e in whole.edges if e.source_id == "card:card-a"]
    assert alone.missing_from("card:card-a") == [m for m in whole.missing_targets if m.source_id == "card:card-a"]


@pytest.fixture
def tracked_project(project: Path, tmp_path: Path):
    _write(tmp_path / f"{MODULE}.py", MODELS)
    sys.path.insert(0, str(tmp_path))
    store = api.init_store(project).store_path
    for model in ("Note", "Card"):
        api.add_model(store, f"{MODULE}:{model}", str(tmp_path))
    api.create_document(store, "Note", project / "notes" / "n2.md", {"title": "Second"}, "n2", str(tmp_path))
    payload = {"id": "card-c", "title": "Card C", "depends_on": ["card-a", "Card:card-missing"], "notes": ["n2"]}
    api.create_document(store, "Card", project / "cards" / "card-c.md", payload, "card-c", str(tmp_path))
    yield project
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


def test_the_store_index_gives_the_edges_of_tracked_documents(tracked_project: Path) -> None:
    graph = ProjectGraph(tracked_project, CONFIG)
    assert graph.store is not None and set(graph.store.tracked) == {"cards/card-c.md", "notes/n2.md"}
    edges = {(e.target_id, e.role) for e in graph.edges_from("card:card-c")}
    assert ("note:notes/n2.md", "notes") in edges
    # `card-a` is no tracked document, so the index leaves it unresolved; it names a node of
    # the project, so it is no finding either. A qualified id naming nothing is reported under
    # the kind of its model.
    assert [(m.target_id, m.provenance_locator) for m in graph.missing_from("card:card-c")] == [("card:card-missing", "frontmatter")]


def test_tracked_documents_agrees_with_doc_status(tracked_project: Path) -> None:
    refs = ["cards/card-c.md", "notes/n2.md", "n2", "Card/card-c", "cards/card-a.md", "nope"]
    store = tracked_project / ".sldb"
    expected = {ref: api.doc_status(store, ref) for ref in refs if api.doc_status(store, ref).exists}
    assert tracked_documents(store, refs) == expected

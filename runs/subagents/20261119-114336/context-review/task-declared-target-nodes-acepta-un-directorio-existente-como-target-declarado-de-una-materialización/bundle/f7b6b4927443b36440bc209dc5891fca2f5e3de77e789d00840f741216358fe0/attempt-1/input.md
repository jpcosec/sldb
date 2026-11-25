FILE:desk/tasks/task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización.md
---
sldb:
  by: agent
  at: '2026-11-17T01:47:21Z'
  authority: generated
  via: create_document
id: task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md
depends_on: []
pills: []
files:
- src/sldb/api/edges/project_graph/declared_target_nodes.py
- tests/api/test_project_graph.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# declared_target_nodes acepta un directorio existente como target declarado de una materialización

## Rationale

_Explain why this task exists or the business driver behind it._

Una MaterializationContractDoc con target_identity igual a un directorio no se convierte en nodo del grafo porque src/sldb/api/edges/project_graph/declared_target_nodes.py exige is_file(); queda como missing_declared_target y graph missing la reporta. En el cierre SV01-SV04 obligó a crear 62 materializaciones para 66 archivos. deskops ya cubre los archivos bajo un directorio por prefijo en su closeout. Origen: desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md.

## Goal

_Describe the concrete result this task must produce._

Un target declarado que es un directorio existente del proyecto produce un nodo del grafo (de directorio) y graph missing no lo reporta; un directorio inexistente sigue siendo missing.

## Scope

_State what is in scope and what is out of scope._

Entra: en declared_target_nodes.py (y file_node.py si el nodo de archivo es la base), aceptar directorios existentes con un nodo de kind directory o el equivalente que ya exista en project_graph; tests en tests/api/test_project_graph.py. CHANGELOG. No entra: expandir el directorio en un nodo por archivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer declared_target_nodes.py, declared_file_targets.py, file_node.py y file_nodes.py. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph_config.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a deskops.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:src/sldb/api/edges/project_graph/declared_target_nodes.py
"""Files that documents declare in a frontmatter field, made nodes so references resolve."""

from __future__ import annotations

from pathlib import Path, PurePosixPath

from sldb.api.edges.project_graph.declared_file_targets import DeclaredFileTargets
from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.file_node import FileNode
from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping
from sldb.api.edges.project_graph.node_provenance import NodeProvenance
from sldb.store.source_guard import aggregate_text


class DeclaredTargetNodes:
    """File nodes for declared targets no path rule made a node and no surface holds."""

    def __init__(self, root: Path, exclusions: FileExclusions, extractor: str) -> None:
        """Keep the (resolved) project root, the exclusions and the extractor name."""
        self.root = root
        self.exclusions = exclusions
        self.extractor = extractor

    def __call__(self, declarations: tuple[DeclaredFileTargets, ...], taken: set[str]) -> list[FileNode]:
        """One node per new declared file, in declaring-document order.

        Args:
            declarations: The declaring fields to read.
            taken: Paths that are already nodes or documents; grows with every node made.

        Returns:
            The new nodes.
        """
        nodes: list[FileNode] = []
        for declaration in declarations:
            for path in self._declaring_documents(declaration):
                target = self._declared_path(path, declaration.field)
                if target is not None and target not in taken:
                    taken.add(target)
                    nodes.append(self._node(target, declaration))
        return nodes

    def _declaring_documents(self, declaration: DeclaredFileTargets) -> list[Path]:
        directory = self.root / declaration.directory
        return sorted(path for path in directory.rglob(declaration.pattern) if path.is_file()) if directory.exists() else []

    def _declared_path(self, document: Path, field: str) -> str | None:
        """The declared repo-relative file, when it is a plain path to an existing project file."""
        value = _field_value(self.root, document, field)
        normalized = value.removeprefix("./") if value else ""
        if not normalized or normalized.startswith("/") or ".." in PurePosixPath(normalized).parts or ":" in normalized:
            return None
        if not (self.root / normalized).resolve().is_relative_to(self.root) or not (self.root / normalized).is_file():
            return None
        return None if self.exclusions.excludes(PurePosixPath(normalized).as_posix()) else normalized

    def _node(self, path: str, declaration: DeclaredFileTargets) -> FileNode:
        provenance = NodeProvenance(path=path, source_kind=declaration.source_kind, extractor=self.extractor)
        return FileNode(id=f"{declaration.kind}:{path}", kind=declaration.kind, identity=path, path=path, file_kind=declaration.file_kind, provenance=provenance)


def _field_value(root: Path, document: Path, field: str) -> str | None:
    try:
        text = aggregate_text(root, document, document.relative_to(root).as_posix())
    except (OSError, UnicodeDecodeError):
        return None
    if text is None:
        return None
    value = (frontmatter_mapping(text) or {}).get(field)
    return value.strip() if isinstance(value, str) and value.strip() else None

FILE:tests/api/test_project_graph.py
"""A project's declared-edge graph: nodes from its files, edges from its store index and its texts.

The project (deskops' desk is the first) only configures where documents live, which files
are nodes and which fields and sections declare references; `ProjectGraph` reads the rest.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.edges.project_graph import (
    DeclaredFileTargets, DocumentSurface, FileExclusions, FileRule, LineMentions, MentionPattern,
    MissingTargetKind, ProjectGraph, ProjectGraphConfig, ReferenceField, SectionMentions,
    extract_document_nodes, extract_file_nodes,
)
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.store.edge_index.compose import invalidate_composed_edge_indexes

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
        DocumentSurface(kind="issue", directory="issues", pattern="*.md", identity="document_id_or_slug", closed='status = "closed"'),
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
    _write(root / "notes" / "n1.md", "---\nstatus: closed\n---\n\n# First note\n")
    _write(root / "issues" / "broken-login.md", "---\nstatus: closed\n---\n\n# Broken Login\n\n## Related cards\n\n- card-a\n")
    _write(root / "issues" / "open-login.md", "---\nstatus: open\n---\n\n# Open Login\n\n## Related cards\n\n- card-a\n")
    _write(root / "src" / "app.py", "")
    _write(root / "src" / "vendored" / "lib.py", "")
    _write(root / "build" / "src" / "x.py", "")
    _write(root / "tests" / "test_app.py", "")
    _write(root / "generated" / "out.py", "")
    return root


def test_nodes_follow_the_surfaces_and_the_file_rules(project: Path) -> None:
    documents = {node.id: node for node in extract_document_nodes(project, CONFIG)}
    assert set(documents) == {"card:card-a", "card:card-b", "note:notes/n1.md", "issue:broken-login", "issue:open-login"}
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
    assert ("issue:broken-login", "card:card-a", "relates", "line:9:related cards", True) in edges
    assert ("issue:open-login", "card:card-a", "relates", "line:9:related cards", None) in edges
    missing = {(m.source_id, m.target_id, m.provenance_locator) for m in graph.extraction().missing_targets}
    assert missing == {
        ("card:card-a", "topic:auth", "frontmatter"), ("card:card-a", "topic:login", "frontmatter"),
        ("card:card-a", "source_file:src/gone.py", "line:11:path"), ("card:card-a", "card:card-zz", "line:16:related cards"),
        ("card:card-a", "topic:yaml-topic", "line:18:yaml"),
    }


def test_closed_is_the_surfaces_predicate_on_the_documents_payload(project: Path) -> None:
    """`status = "closed"` closes the issue that holds it: not the open one, nor a note (its surface has no `closed`)."""
    texts = ProjectGraph(project, CONFIG).texts
    assert texts.is_history("issue", texts.text("issues/broken-login.md")) is True
    assert texts.is_history("issue", texts.text("issues/open-login.md")) is None
    assert texts.is_history("note", texts.text("notes/n1.md")) is None
    assert texts.is_history("issue", "# No status\n") is None


def test_edges_to_gives_the_mention_with_its_path_and_line(project: Path) -> None:
    graph = ProjectGraph(project, CONFIG)
    incoming = [(e.source_id, e.role, e.provenance_path, e.provenance_locator, e.record) for e in graph.edges_to("source_file:src/app.py")]
    assert incoming == [("card:card-a", "touches", "cards/card-a.md", "line:11:path", None), ("card:card-b", "touches", "cards/card-b.md", "line:8:path", True)]
    assert graph.edges_to("card:card-a") == [e for e in graph.extraction().edges if e.target_id == "card:card-a"]
    assert graph.edges_to("card:card-a")[0].to_dict() == graph.edges_from("issue:broken-login")[0].to_dict()
    assert graph.edges_to("nobody:here") == []


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


def test_a_tracked_document_is_judged_on_its_indexed_payload(tracked_project: Path) -> None:
    """The index projection carries `title` (a body field); the frontmatter alone would not."""
    texts = ProjectGraph(tracked_project, CONFIG).texts
    assert texts.payload_of(texts.text("cards/card-c.md"))["title"] == "Card C"
    assert texts.payload_of(texts.text("cards/card-a.md"))["id"] == "card-a"


@pytest.fixture
def declared_project(tracked_project: Path) -> Path:
    """The tracked project with `project_graph` declared in its `store.yaml`."""
    store = tracked_project / ".sldb"
    declaration = declare_store(store, tracked_project).model_copy(update={"project_graph": CONFIG.to_mapping()})
    save_declaration(store, declaration)
    return tracked_project


def _count_walks(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    counts = {"walk": 0, "rglob": 0}
    walk, rglob = os.walk, Path.rglob

    def counted_walk(*args, **kwargs):
        counts["walk"] += 1
        return walk(*args, **kwargs)

    def counted_rglob(self, *args, **kwargs):
        counts["rglob"] += 1
        return rglob(self, *args, **kwargs)

    monkeypatch.setattr(os, "walk", counted_walk)
    monkeypatch.setattr(Path, "rglob", counted_rglob)
    return counts


def test_the_declared_graph_is_read_from_store_yaml_without_any_callable(declared_project: Path) -> None:
    graph = api.project_graph(declared_project / ".sldb")
    assert graph.config == CONFIG and graph.config.closed_document is None
    assert {node.id for node in graph.nodes.documents} >= {"card:card-a", "card:card-c", "issue:broken-login"}
    assert [e.provenance_locator for e in graph.edges_to("source_file:src/app.py")] == ["line:11:path", "line:8:path"]


def test_a_second_query_without_changes_walks_nothing(declared_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = declared_project / ".sldb"
    counts = _count_walks(monkeypatch)
    first = api.project_graph(store)
    assert counts["walk"] > 0
    counts.update(walk=0, rglob=0)
    assert api.project_graph(store) is first
    assert first.edges_to("source_file:src/app.py") and first.extraction().missing_targets
    assert counts == {"walk": 0, "rglob": 0}


def test_touching_an_included_file_makes_the_next_query_recalculate(declared_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    store = declared_project / ".sldb"
    first = api.project_graph(store)
    assert first.edges_to("test_file:tests/test_app.py") == []
    counts = _count_walks(monkeypatch)
    card = declared_project / "cards" / "card-a.md"
    card.write_text(card.read_text(encoding="utf-8") + "\nAlso tests/test_app.py.\n", encoding="utf-8")
    second = api.project_graph(store)
    assert second is not first and counts["walk"] > 0
    assert [e.provenance_locator for e in second.edges_to("source_file:src/app.py")] == ["line:11:path", "line:8:path"]
    counts.update(walk=0, rglob=0)
    assert api.project_graph(store) is second and counts["walk"] == 0


def test_a_new_file_in_a_walked_directory_and_a_changed_declaration_recalculate(declared_project: Path) -> None:
    store = declared_project / ".sldb"
    first = api.project_graph(store)
    _write(declared_project / "src" / "new.py", "")
    second = api.project_graph(store)
    assert second is not first and "source_file:src/new.py" in {node.id for node in second.nodes.files}
    declaration = declare_store(store, declared_project).model_copy(update={"project_graph": CONFIG.model_copy(update={"surfaces": CONFIG.surfaces[:2]}).to_mapping()})
    save_declaration(store, declaration)
    assert "issue:broken-login" not in {node.id for node in api.project_graph(store).nodes.documents}


def test_the_existing_cache_invalidation_drops_the_memoized_graph(declared_project: Path) -> None:
    store = declared_project / ".sldb"
    first = api.project_graph(store)
    assert api.project_graph(store) is first
    invalidate_composed_edge_indexes()
    assert api.project_graph(store) is not first

FILE:instruccion
Cold-bundle de la tarea task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph_config.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast


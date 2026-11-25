FILE:desk/tasks/task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com.md
---
sldb:
  by: agent
  at: '2026-11-17T14:48:10Z'
  authority: generated
  via: save_document_payload
id: task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/links.py
- tests/test_links.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El scan de enlaces ignora el contenido de los bloques de código (fenced e inline) y no los informa como enlaces rotos

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, el scan de enlaces de un documento real lista dos veces 'target' como enlace roto, y los dos vienen de ejemplos dentro de bloques de código del Markdown. Origen: desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md.

## Goal

_Describe the concrete result this task must produce._

El scan de enlaces de sldb (comando sldb links y la API que usa) no cuenta como enlace nada que esté dentro de un bloque de código cercado ni de un código en línea; los enlaces reales se siguen detectando igual.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar el parser de enlaces que usa src/sldb/cli/commands/links.py y excluir los bloques de código cercados (con backticks o tildes) y el código en línea; tests en tests/test_links.py con un documento que tiene enlaces reales y ejemplos dentro de bloques de código. CHANGELOG. No entra: otros tipos de referencia.

Precisiones (coordinador, corrección 2, 2026-11-17): un fence puede abrirse en la misma línea que el marcador de un ítem de lista ("- ```", "1. ```python", "* ~~~"); su apertura se mide en la columna de contenido del ítem y su cierre puede venir indentado a esa columna. Un cierre indentado sin apertura vista no abre un bloque nuevo que se trague el resto del archivo. Tests: los cuatro casos de runs/subagents/20261116-test-lk-c1/result-summary.md (dos con enlaces reales después del bloque y dos con [[...]] dentro del bloque), cada uno contrastado con markdown-it-py commonmark si está instalado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer links.py y el parser que llama. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a sldb-ui.

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

FILE:src/sldb/cli/commands/links.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from sldb.cli.store_context import get_store_context
from sldb.cli.commands.links_all import batch_requested, recover_all
from sldb.cli.utils import write_text
from sldb.links import compose_document, recover_links, resolve_document_input


class LinkCLI:
    """Handles link recovery and document composition."""

    def recover(self, args: Any) -> int:
        if batch_requested(args): return recover_all(args)
        sp, root = get_store_context(args.store)
        res = recover_links(
            resolve_document_input(args.doc, sp), sp,
            include_transclusions=args.include_transclusions, depth=args.depth,
        )
        if args.links_only:
            return self._print_links_only(res)
        self._print_recovery(res, args.format)
        return 0 if not res.get("unresolved") else 1

    def _print_links_only(self, res: dict) -> int:
        targets = sorted(set(link["target"] for link in res.get("links", [])))
        for t in targets:
            print(t)
        return 0 if not res.get("unresolved") else 1

    def _print_recovery(self, res: dict, fmt: str) -> None:
        if fmt == "text":
            for link in res.get("links", []):
                self._print_link_text(link)
        elif fmt == "json":
            print(json.dumps(res, indent=2))
        else:
            print(yaml.dump(res, allow_unicode=True, sort_keys=False))

    def _print_link_text(self, link: dict) -> None:
        resolved = "ok" if link["resolved"] else "FAIL"
        if link.get("predicate"):
            w5h1 = f"[{link['w5h1_type']}]" if link.get("w5h1_type") else ""
            print(f"{link['kind']}: [{link['predicate']}]{w5h1} {link['target']} [{resolved}]")
        else:
            print(f"{link['kind']}: {link['target']} [{resolved}]")

    def compose(self, args: Any) -> int:
        sp, root = get_store_context(args.store)
        doc = resolve_document_input(args.doc, sp)
        res = compose_document(doc, sp, links_base=self._links_base(args, doc))
        self._write_composed(args, res)
        return 0 if not res["unresolved"] else 1

    @staticmethod
    def _links_base(args: Any, doc: Path) -> Path | None:
        if not args.render_links: return None
        return doc.parent if args.output == "-" else Path(args.output).resolve().parent

    def _write_composed(self, args: Any, res: dict) -> None:
        if args.format == "markdown":
            write_text(args.output, res["markdown"] + "\n")
        elif args.format == "yaml":
            write_text(args.output, yaml.safe_dump(res, sort_keys=False, allow_unicode=True))
        else:
            write_text(args.output, json.dumps(res, indent=2))

FILE:tests/test_links.py
import json

from pathlib import Path
from textwrap import dedent

from sldb.cli import main as cli_main


def _write_models(base: Path) -> str:
    module = base / "link_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev•body⸥""".strip()
    title: str = Field(description="Document title.")
    body: str = Field(description="Document body.")


class RootDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

See [[⸢rev•linked_doc⸥]] for background.

![[⸢rev•transclusion_doc⸥]]""".strip()
    title: str = Field(description="Document title.")
    linked_doc: str = Field(description="Tracked linked document name.")
    transclusion_doc: str = Field(description="Tracked transcluded document name.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def test_recover_and_compose_links(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            str(root),
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert recovered["root"] == "root"
    assert recovered["links"][0]["target"] == "concept"
    assert recovered["links"][0]["kind"] == "link"
    assert recovered["links"][0]["resolved"] is True
    assert recovered["links"][1]["target"] == "constraints"
    assert recovered["links"][1]["kind"] == "transclusion"
    assert recovered["unresolved"] == []

    capsys.readouterr()
    rc = cli_main(["docs", "compose", str(root), "--store", str(store)])
    composed = capsys.readouterr().out
    assert rc == 0
    assert "See [[concept]] for background." in composed
    assert "# Constraints" in composed
    assert "Always validate first." in composed


def test_docs_recover_and_compose_accept_tracked_doc_names_and_yaml(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--name",
                "root-doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert {link["target"] for link in recovered["links"]} == {"concept", "constraints"}

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "compose",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "yaml",
            "-o",
            "-",
        ]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert out.lstrip().startswith("root: root")
    assert "transclusions:" in out


# =============================================================================
# Tests for predicate links (5W1H+)
# =============================================================================


def test_parse_predicate_links():
    """Test parsing of [predicate:: [[target]]] syntax."""
    from sldb.links import parse_links

    markdown = dedent("""
    This task [implements:: [[spec-001]]].
    Another [is_solved_by:: [[solution-002]]].
    [custom_predicate:: [[some-doc]]].
    """)
    links = parse_links(
        markdown,
        {"implements": "HOW", "is_solved_by": "HOW"},
    )

    assert len(links) == 3

    # First predicate link
    assert links[0].target == "spec-001"
    assert links[0].predicate == "implements"
    assert links[0].w5h1_type == "HOW"
    assert links[0].kind == "predicate_link"

    # Second predicate link with different predicate
    assert links[1].target == "solution-002"
    assert links[1].predicate == "is_solved_by"
    assert links[1].w5h1_type == "HOW"

    # Custom predicate gets CUSTOM type
    assert links[2].target == "some-doc"
    assert links[2].predicate == "custom_predicate"
    assert links[2].w5h1_type == "CUSTOM"


def test_parse_links_uses_injected_predicate_axes():
    """Predicate classification comes from the caller, not hardcoded data."""
    from sldb.links import parse_links

    links = parse_links(
        "[depends_on:: [[target]]] [unknown:: [[other]]]",
        {"depends_on": "DEPENDENCY"},
    )

    assert links[0].predicate == "depends_on"
    assert links[0].w5h1_type == "DEPENDENCY"
    assert links[1].predicate == "unknown"
    assert links[1].w5h1_type == "CUSTOM"


def test_parse_mixed_links_with_predicates():
    """Test parsing of documents with both regular links and predicate links."""
    from sldb.links import parse_links

    markdown = dedent("""
    See [[background]] for context.

    This solution [implements:: [[spec-v2]]] and
    [grounded_by:: [[research-paper]]].

    Also check [[related-work]].
    """)
    links = parse_links(
        markdown,
        {"implements": "HOW", "grounded_by": "PROVENANCE"},
    )

    # 2 predicate links + 2 regular links = 4 total
    assert len(links) == 4

    # Check kinds
    kinds = {link.kind for link in links}
    assert "link" in kinds
    assert "predicate_link" in kinds

    # Check specific predicates
    predicate_links = [link for link in links if link.kind == "predicate_link"]
    assert len(predicate_links) == 2
    assert predicate_links[0].predicate == "implements"
    assert predicate_links[1].predicate == "grounded_by"


def test_predicate_links_with_transclusion_bang():
    """Test that [predicate:: ![[target]]] is supported."""
    from sldb.links import parse_links

    markdown = "[implements:: ![[embedded-spec]]]"
    links = parse_links(markdown, {"implements": "HOW"})

    assert len(links) == 1
    assert links[0].target == "embedded-spec"
    assert links[0].predicate == "implements"
    # Bang inside predicate link means transclusion kind
    assert links[0].kind == "transclusion"


def test_resolve_predicate_link(tmp_path):
    """Test resolving a predicate link via relative path."""
    from sldb.links import resolve_link_target

    # Create a document alongside current doc
    docs = tmp_path / "docs"
    docs.mkdir()
    spec_doc = docs / "spec-001.md"
    spec_doc.write_text("# Spec 001\n", encoding="utf-8")

    resolved = resolve_link_target(
        "docs/spec-001.md",
        tmp_path / "current.md",
        None,  # No store, use relative path
        predicate="implements",
        w5h1_type="HOW",
    )

    assert resolved.resolved is True
    assert resolved.kind == "predicate_link"
    assert resolved.predicate == "implements"
    assert resolved.w5h1_type == "HOW"
    assert resolved.source == "path"


def test_recover_predicate_links_cli(tmp_path, capsys):
    """Test that CLI recover command shows predicate info in JSON format."""
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    spec = tmp_path / "spec.md"
    spec.write_text("# Spec\n", encoding="utf-8")
    research = tmp_path / "research.md"
    research.write_text("# Research\n", encoding="utf-8")
    task = tmp_path / "task.md"
    # Use resolved links to different documents
    task.write_text(
        "# Task\n\n" + "[implements:: [[spec]]]\n" + "[grounded_by:: [[research]]]",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(spec),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(research),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(task),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            str(task),
            "--store",
            str(store),
            "--format",
            "json",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)

    assert rc == 0
    predicate_links = [
        link for link in recovered["links"] if link["kind"] == "predicate_link"
    ]
    assert len(predicate_links) == 2

    predicates = {link["predicate"] for link in predicate_links}
    assert predicates == {"implements", "grounded_by"}

    # Check 5W1H types
    implements_link = next(
        link for link in predicate_links if link["predicate"] == "implements"
    )
    assert implements_link["w5h1_type"] == "HOW"

    grounded_link = next(
        link for link in predicate_links if link["predicate"] == "grounded_by"
    )
    assert grounded_link["w5h1_type"] == "PROVENANCE"


# =============================================================================
# Code is not scanned for links (fenced, indented and inline code)
# =============================================================================

CODE_EXAMPLES_DOC = """# Guía de enlaces

Ver [[concept]] y [implements:: [[spec-001]]].

```markdown
Un enlace se escribe [[target]] y una transclusión ![[target]].
```

~~~~
[depends_on:: [[target]]]
~~~
sigue dentro: el cierre de tildes es más corto que la apertura [[target]]
~~~~

    [[target]] en un bloque indentado

- un ítem de lista con [[item-link]]

    [[nested-link]] dentro del ítem no es código

Usa `[[target]]` o ``[[target]] con ` adentro``; un ` suelto no abre código, y [[after-tick]] cuenta.

Cierre: [[closing]].

```
bloque sin cerrar: [[target]]
"""


def test_parse_links_skips_code():
    from sldb.links import parse_links

    links = parse_links(CODE_EXAMPLES_DOC, {"implements": "HOW"})

    assert [(link.target, link.kind) for link in links] == [
        ("spec-001", "predicate_link"),
        ("concept", "link"),
        ("item-link", "link"),
        ("nested-link", "link"),
        ("after-tick", "link"),
        ("closing", "link"),
    ]


def test_parse_links_fence_rules():
    from sldb.links import parse_links

    def targets(markdown):
        return [link.target for link in parse_links(markdown)]

    assert targets("```\n[[a]]\n```\n[[b]]\n") == ["b"]
    assert targets("~~~python\n[[a]]\n~~~\n[[b]]\n") == ["b"]
    assert targets("````\n[[a]]\n```\n[[b]]\n````\n[[c]]\n") == ["c"]
    assert targets("```\n[[a]]\n~~~\n[[b]]\n") == []
    assert targets("```x``` [[a]]\n") == ["a"]
    assert targets("texto\n    [[a]] continúa el párrafo\n") == ["a"]
    assert targets("texto\n\n\t[[a]]\n\n[[b]]\n") == ["b"]
    assert targets("`` [[a]] ` `` [[b]] ```[[c]]`` [[d]]\n") == ["b", "c", "d"]
    assert targets("`abre\n\n[[a]] cierra`\n") == ["a"]


def test_docs_recover_ignores_links_in_code(tmp_path, capsys):
    """The sldb-ui case: example links inside code are not reported as broken."""
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", "link_models:NoteDoc", "--store", str(store), "--pythonpath", pythonpath]) == 0
    for name in ("concept", "item-link", "nested-link", "after-tick", "closing"):
        note = tmp_path / f"{name}.md"
        note.write_text(f"# {name}\n\nBody.\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(note), "--model", "NoteDoc", "--store", str(store), "--pythonpath", pythonpath]) == 0
    doc = tmp_path / "guide.md"
    doc.write_text(CODE_EXAMPLES_DOC.replace("[implements:: [[spec-001]]]", "[[concept]]"), encoding="utf-8")

    capsys.readouterr()
    rc = cli_main(["docs", "recover", str(doc), "--store", str(store), "--format", "json", "--include-transclusions"])
    recovered = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert [link["target"] for link in recovered["links"]] == ["concept", "item-link", "nested-link", "after-tick", "closing"]
    assert all(link["resolved"] for link in recovered["links"])
    assert recovered["unresolved"] == []


def _commonmark_targets(markdown):
    """Link targets outside code per markdown-it-py in commonmark mode, or None if it is not installed."""
    import re

    try:
        from markdown_it import MarkdownIt
    except ImportError:
        return None
    html = re.sub(r"<code[^>]*>.*?</code>", "", MarkdownIt("commonmark").render(markdown.replace("\r\n", "\n")), flags=re.S)
    return [m.group(1).strip() for m in re.finditer(r"\[\[([^\]]+)\]\]", html)]


def _assert_targets(markdown, expected):
    from sldb.links import parse_links

    assert [link.target for link in parse_links(markdown)] == expected
    reference = _commonmark_targets(markdown)
    assert reference is None or reference == expected


def test_parse_links_indented_code_in_list_item():
    """Code inside a list item starts 4 columns past the item's content, also in a sub-item."""
    _assert_targets("- item\n\n        [[code8]]\n\n- b [[real]]\n", ["real"])
    _assert_targets("- item\n  - sub\n\n          [[c]]\n", [])
    _assert_targets("- item\n  - sub\n\n      [[para]]\n", ["para"])
    _assert_targets("1. item\n\n       [[c]]\n\n[[d]]\n\n    [[e]]\n", ["d"])


def test_parse_links_escaped_backtick_is_text():
    _assert_targets("\\`[[b]]\\`\n", ["b"])
    _assert_targets("\\``[[a]]` [[b]]\n", ["b"])
    _assert_targets("\\\\`[[a]]` [[b]]\n", ["b"])


def test_parse_links_crlf_line_ends():
    _assert_targets("```\r\n[[a]]\r\n```\r\n[[b]]\r\n", ["b"])
    _assert_targets("~~~\r\n[[a]]\r\n~~~ \r\n[[b]]\r\n", ["b"])
    _assert_targets("`[[a]]\r\n\r\n[[b]]` [[c]]\r\n", ["a", "b", "c"])

FILE:instruccion
Cold-bundle de la tarea task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast


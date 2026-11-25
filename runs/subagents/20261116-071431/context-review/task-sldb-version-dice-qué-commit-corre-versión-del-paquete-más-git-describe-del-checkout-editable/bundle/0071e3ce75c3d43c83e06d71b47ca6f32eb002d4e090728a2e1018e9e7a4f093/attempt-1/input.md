FILE:desk/tasks/task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable.md
---
sldb:
  by: agent
  at: '2026-11-16T06:06:05Z'
  authority: generated
  via: save_document_payload
id: task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-dos-instalaciones-de-sldb-y-la-versión-no-dice-qué-commit-corre.md
depends_on: []
pills: []
files:
- src/sldb/store/package_version.py
- src/sldb/cli/parser.py
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb --version dice qué commit corre (versión del paquete más git describe del checkout editable)

## Rationale

_Explain why this task exists or the business driver behind it._

En robocop hubo dos instalaciones de sldb (una editable sobre el checkout principal con cambios ajenos, otra sobre ~/herramientas/sldb) y las dos decían 0.1.13, aunque git describe daba v0.1.13-283-gb965c62d: ningún comando dice qué commit corre. La instalación ya quedó en una sola (uv tool deskops, editable sobre /home/robocop/herramientas/sldb); falta lo de sldb. src/sldb/store/package_version.py devuelve solo la versión del pyproject y la CLI (src/sldb/cli/parser.py) no tiene --version. Origen: desk/inbox/inbox-note-dos-instalaciones-de-sldb-y-la-versión-no-dice-qué-commit-corre.md.

## Goal

_Describe the concrete result this task must produce._

`sldb --version` imprime una línea "sldb <versión> (<git describe --always --dirty> at <ruta del checkout>)" cuando corre desde un checkout git, y "sldb <versión>" cuando corre desde un paquete instalado sin .git; exit 0.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/package_version.py una función source_revision() -> str | None que, si el pyproject encontrado por _source_checkout_version está en un directorio con .git (archivo o carpeta, para worktrees), corre `git -C <dir> describe --tags --always --dirty` con subprocess (timeout 2 s) y devuelve su salida, o None si git falla o no está; en src/sldb/cli/parser.py el argumento global --version con action que imprime la línea de Goal. Tests en tests/test_cli_v2.py: --version sale con 0 y empieza con "sldb "; con source_revision parcheada a None no hay paréntesis; con un valor fijo aparece entre paréntesis. CHANGELOG.md. No entra: cambiar producer.version de los sellos de procedencia, decidir qué instalación es la de referencia (ya resuelto: una sola instalación), limpiar los review dirs huérfanos del desk.

Precisiones (preflight-1): el comando git es exactamente `git -C <dir> describe --tags --always --dirty` (con --tags, también en Goal). <dir> y la "ruta del checkout" son el directorio que contiene el pyproject.toml que encontró _source_checkout_version (una función existente de package_version.py que devuelve la versión del pyproject del checkout o None); hay que hacer que también devuelva o exponga ese directorio, o buscarlo con el mismo recorrido. subprocess.run(..., capture_output=True, text=True, timeout=2, check=False); si returncode != 0, salida vacía, o FileNotFoundError/TimeoutExpired, source_revision devuelve None. Línea exacta: "sldb <versión> (<describe> at <dir>)" o "sldb <versión>". En los tests se parchea sldb.store.package_version.source_revision con monkeypatch y se llama a sldb.cli.main(["--version"]) capturando stdout.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/package_version.py y src/sldb/cli/parser.py (construcción del parser raíz). 2) Agregar source_revision. 3) Agregar --version con una argparse.Action propia que imprime y sale. 4) Tests. 5) Probar a mano `sldb --version` desde el checkout.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_envelope.py
- PYTHONPATH=src python -m sldb --version

## Done When

_Name the observable condition that makes the task complete._

Los tests pasan; `PYTHONPATH=src python -m sldb --version` desde el checkout imprime la versión con el describe entre paréntesis; CHANGELOG y commit.

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

FILE:src/sldb/store/package_version.py
"""The real package version, for provenance stamps such as `producer.version`."""

from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

_DIST_NAME = "structuredLanguageDB"


def _source_checkout_version() -> str | None:
    """Version in the pyproject.toml above `src/`, when running from a source tree."""
    for parent in Path(__file__).resolve().parents[:5]:
        pyproject = parent / "pyproject.toml"
        if pyproject.is_file():
            text = pyproject.read_text(encoding="utf-8")
            if f'name = "{_DIST_NAME}"' in text:
                match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
                return match.group(1) if match else None
    return None


def package_version() -> str:
    """Real package version: the source checkout's pyproject, else installed metadata."""
    checkout = _source_checkout_version()
    if checkout:
        return checkout
    try:
        return version(_DIST_NAME)
    except PackageNotFoundError:
        return "unknown"

FILE:src/sldb/cli/parser.py
from __future__ import annotations
import argparse
from sldb.cli.parsers.core import build_parser

__all__ = ["build_parser"]

FILE:tests/test_cli_v2.py
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

from sldb.cli import main as cli_main
from sldb.store.io import load_documents_index, load_models_index, load_store_index


def _write_models(base: Path) -> str:
    sys.modules.pop("cli_v2_models", None)
    module = base / "cli_v2_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class RoadmapDoc(StructuredNLDoc):
    __semantics__ = {"type": ["documentation", "Readme"]}
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥

## Tasks

- ⸢rev,list•tasks⸥

## Semantic Tags

- ⸢rev,list•semantic_tags⸥
""".strip()
    title: str = Field(description="Document title.")
    status: str = Field(description="Workflow status.")
    tasks: list[str] = Field(description="Task items.")
    semantic_tags: list[str] = Field(description="Semantic tags.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def _write_federated_models(base: Path) -> str:
    sys.modules.pop("federated_models", None)
    module = base / "federated_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class RequestDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev,markdown•body⸥
""".strip()
    title: str = Field(description="Request title.")
    body: str = Field(description="Request body.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def _setup_store(tmp_path: Path) -> tuple[Path, str]:
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "cli_v2_models:RoadmapDoc",
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
                "create",
                "--model",
                "RoadmapDoc",
                "-o",
                str(root / "roadmap.md"),
                json.dumps(
                    {
                        "title": "Roadmap",
                        "status": "draft",
                        "tasks": ["Ship CLI", "Write docs"],
                        "semantic_tags": ["project.sldb.database"],
                    }
                ),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    return store, pythonpath


def _write_template(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def _model_index_path(store: Path, model_name: str) -> Path:
    entry = next(m for m in load_store_index(store).models if m.name == model_name)
    return store.parent / entry.models_index


def test_docs_create_accepts_long_inline_json_payload(tmp_path):
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "cli_v2_models:RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    long_title = "x" * 300
    output = root / "long-inline.md"
    assert (
        cli_main(
            [
                "docs",
                "create",
                "--model",
                "RoadmapDoc",
                "-o",
                str(output),
                json.dumps(
                    {
                        "title": long_title,
                        "status": "draft",
                        "tasks": ["Ship CLI"],
                        "semantic_tags": ["project.sldb.database"],
                    }
                ),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    assert output.exists()
    assert f"# {long_title}" in output.read_text(encoding="utf-8")


def test_docs_create_accepts_linked_store_alias(tmp_path, monkeypatch):
    pythonpath = _write_federated_models(tmp_path)
    central = tmp_path / "central"
    target = tmp_path / "target"
    central.mkdir()
    target.mkdir()
    central_store = central / ".sldb"
    target_store = target / ".sldb"

    assert cli_main(["stores", "init", "--path", str(central)]) == 0
    assert cli_main(["stores", "init", "--path", str(target)]) == 0
    monkeypatch.chdir(central)
    assert (
        cli_main(
            [
                "models",
                "add",
                "federated_models:RequestDoc",
                "--store",
                str(target_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(target_store),
                "--name",
                "target",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )

    assert (
        cli_main(
            [
                "docs",
                "create",
                "--store",
                "target",
                "--model",
                "RequestDoc",
                "-o",
                "desk/inbox/request-123.md",
                json.dumps({"title": "Need review", "body": "Please review this."}),
                "--pythonpath",
                pythonpath,
            ],
        )
        == 0
    )

    output = target / "desk" / "inbox" / "request-123.md"
    assert output.exists()
    assert "# Need review" in output.read_text(encoding="utf-8")
    docs_index = load_documents_index(
        target / ".sldb" / "core" / "documents" / "RequestDoc.yaml"
    )
    assert [doc.path for doc in docs_index.documents] == [
        "desk/inbox/request-123.md"
    ]


def test_docs_create_uses_model_from_linked_store_namespace(tmp_path, monkeypatch):
    pythonpath = _write_federated_models(tmp_path)
    central = tmp_path / "central"
    models_repo = tmp_path / "deskops"
    target = tmp_path / "target"
    central.mkdir()
    models_repo.mkdir()
    target.mkdir()
    central_store = central / ".sldb"
    models_store = models_repo / ".sldb"
    target_store = target / ".sldb"

    assert cli_main(["stores", "init", "--path", str(central)]) == 0
    assert cli_main(["stores", "init", "--path", str(models_repo)]) == 0
    assert cli_main(["stores", "init", "--path", str(target)]) == 0
    monkeypatch.chdir(central)
    assert (
        cli_main(
            [
                "models",
                "add",
                "federated_models:RequestDoc",
                "--store",
                str(models_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(models_store),
                "--name",
                "deskops",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "stores",
                "add",
                str(target_store),
                "--name",
                "target",
                "--store",
                str(central_store),
            ]
        )
        == 0
    )

    assert (
        cli_main(
            [
                "docs",
                "create",
                "--store",
                "target",
                "--model",
                "deskops:RequestDoc",
                "-o",
                "desk/inbox/request-456.md",
                json.dumps({"title": "Need model", "body": "Use deskops model."}),
                "--pythonpath",
                pythonpath,
            ],
        )
        == 0
    )

    output = target / "desk" / "inbox" / "request-456.md"
    assert output.exists()
    assert "Use deskops model." in output.read_text(encoding="utf-8")
    docs_index = load_documents_index(
        target / ".sldb" / "core" / "documents" / "RequestDoc.yaml"
    )
    assert [doc.path for doc in docs_index.documents] == [
        "desk/inbox/request-456.md"
    ]


def test_help_topics(capsys):
    assert cli_main(["--help"]) == 0
    out = capsys.readouterr().out
    assert "SLDB's main workflow is:" in out
    assert "Primary surfaces:" in out
    assert "raw-find" not in out
    assert "extract, render, validate   Direct model-first operations without a store" in out

    original_argv = sys.argv[:]
    try:
        sys.argv = ["sldb", "--help"]
        assert cli_main() == 0
        out = capsys.readouterr().out
        assert "SLDB's main workflow is:" in out
        assert "raw-find" not in out
    finally:
        sys.argv = original_argv

    assert cli_main(["help"]) == 0
    out = capsys.readouterr().out
    assert "not `bash sldb ...`" in out
    assert "explore   Deep markdown docs and docstring search" in out
    assert "faq       Question-oriented onboarding answers" in out
    assert "inbox     Log unclear points or suggestions to the active project desk" in out

    assert cli_main(["help", "fields"]) == 0
    out = capsys.readouterr().out
    assert "fields append" in out
    assert "CRUD" in out
    capsys.readouterr()
    assert cli_main(["help", "sections"]) == 0
    out = capsys.readouterr().out
    assert "sections show" in out
    assert "sections find" in out
    assert "sections fields" in out
    capsys.readouterr()
    assert cli_main(["help", "explore"]) == 0
    out = capsys.readouterr().out
    assert "Deep search over markdown docs and Python docstrings" in out
    assert "--source all|docs|docstrings" in out

    assert cli_main(["find", "--help"]) == 0
    out = capsys.readouterr().out
    assert "Use `physical` for names, paths, section titles, and" in out.replace("\n", " ")
    assert "sldb find roadmap --in physical --type doc" in out
    assert "Typical shapes:" in out

    assert cli_main(["docs", "--help"]) == 0
    out = capsys.readouterr().out
    assert "`recover` and `compose` work on explicit Markdown links and" in out.replace("\n", " ")
    assert "Resolve [[links]] and report their targets." in out
    assert "Expand ![[transclusions]] into composed Markdown." in out

    assert cli_main(["docs", "recover", "--help"]) == 0
    out = capsys.readouterr().out
    assert "sldb docs recover roadmap --store .sldb" in out

    assert cli_main(["docs", "compose", "--help"]) == 0
    out = capsys.readouterr().out
    assert "Output path or - for stdout" in out

    assert cli_main(["models", "--help"]) == 0
    out = capsys.readouterr().out
    assert "list                List registered models." in out

    assert cli_main(["help", "models"]) == 0
    out = capsys.readouterr().out
    assert "models list --store .sldb" in out


def test_faq_lists_and_selects_questions(capsys):
    # The repo's FAQ by path: finding it through the repo's store needs that (derived) store built.
    faq = ["--faq-path", str(Path(__file__).resolve().parents[1] / "docs" / "faq.md")]
    assert cli_main(["faq", *faq]) == 0
    out = capsys.readouterr().out
    assert "SLDB FAQ questions:" in out
    assert "What exactly is a store?" in out

    assert cli_main(["faq", "store", *faq]) == 0
    out = capsys.readouterr().out
    assert "What exactly is a store?" in out
    assert "A store is SLDB's metadata workspace" in out


def test_inbox_writes_desk_note(tmp_path, capsys):
    desk_root = tmp_path / "desk"
    assert (
        cli_main(
            [
                "inbox",
                "The docs should explain tracked doc names more clearly.",
                "--kind",
                "suggestion",
                "--title",
                "tracked doc names",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "Wrote" in out
    inbox_files = list((desk_root / "inbox").glob("*.md"))
    assert len(inbox_files) == 1
    text = inbox_files[0].read_text(encoding="utf-8")
    assert "kind: suggestion" in text
    assert "# tracked doc names" in text
    assert "The docs should explain tracked doc names more clearly." in text


def test_inbox_rejects_title_only_placeholder(tmp_path):
    desk_root = tmp_path / "desk"
    with pytest.raises(SystemExit) as exc:
        cli_main(
            [
                "inbox",
                "Repo-targeted note",
                "--kind",
                "unclear",
                "--desk-root",
                str(desk_root),
            ]
        )
    assert "Inbox note needs more detail" in str(exc.value)


def test_models_list_lists_registered_models(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(["models", "list", "--store", str(store)])
        == 0
    )
    out = capsys.readouterr().out
    assert "Models in" in out
    assert "RoadmapDoc | cli_v2_models:RoadmapDoc" in out
    assert "1 docs" in out

    assert (
        cli_main(["models", "list", "--store", str(store), "--format", "json"])
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["models"][0]["name"] == "RoadmapDoc"
    assert payload["models"][0]["documents"] == 1


def test_models_list_fails_on_no_store_and_no_global(tmp_path, capsys, monkeypatch):
    project = tmp_path / "no-store-project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    with pytest.raises(SystemExit) as exc:
        cli_main(["models", "list"])
    assert "No local .sldb store found" in str(exc.value)
    assert "No global store exists" in str(exc.value)
    assert "sldb stores init --path ." in str(exc.value)


def test_models_list_falls_back_to_global_when_no_local(tmp_path, capsys, monkeypatch):
    project = tmp_path / "no-store-project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    home_store_root = Path.home()
    (home_store_root / ".sldb" / "core").mkdir(parents=True, exist_ok=True)
    (home_store_root / ".sldb" / "runtime").mkdir(parents=True, exist_ok=True)
    from sldb.store.io import save_store_index
    from sldb.store.models import StoreIndex

    save_store_index(home_store_root / ".sldb", StoreIndex())

    result = cli_main(["models", "list"])
    assert result == 0
    stderr = capsys.readouterr().err
    assert "falling back to global store" in stderr


def test_inbox_lists_and_shows_notes(tmp_path, capsys):
    desk_root = tmp_path / "desk"
    assert (
        cli_main(
            [
                "inbox",
                "Semantic docs are still a bit unclear.",
                "--kind",
                "unclear",
                "--title",
                "semantic docs",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "inbox",
                "Add more examples for compose.",
                "--kind",
                "suggestion",
                "--title",
                "compose examples",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert cli_main(["inbox", "--list", "--desk-root", str(desk_root)]) == 0
    out = capsys.readouterr().out
    assert "semantic docs" in out
    assert "compose examples" in out

    assert (
        cli_main(
            [
                "inbox",
                "--show",
                "compose-examples",
                "--desk-root",
                str(desk_root),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "# compose examples" in out
    assert "kind: suggestion" in out
    assert "Add more examples for compose." in out


def test_inbox_defaults_to_local_store_project_desk(tmp_path, capsys, monkeypatch):
    project = tmp_path / "target-project"
    project.mkdir()
    assert cli_main(["stores", "init", "--path", str(project)]) == 0
    capsys.readouterr()

    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.chdir(other)

    assert (
        cli_main(
            [
                "inbox",
                "Route this to the target project desk.",
                "--store",
                str(project / ".sldb"),
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert str(project / "desk" / "inbox") in out
    note_files = list((project / "desk" / "inbox").glob("*.md"))
    assert len(note_files) == 1
    assert not (other / "desk").exists()


def test_inbox_auto_tracks_when_model_registered(tmp_path, capsys, monkeypatch):
    project = tmp_path / "target-project"
    project.mkdir()
    assert cli_main(["stores", "init", "--path", str(project)]) == 0
    capsys.readouterr()

    repo_pythonpath = str(Path(__file__).resolve().parent)
    assert (
        cli_main(
            [
                "models",
                "add",
                "inbox_note_fixture_models:InboxNoteDoc",
                "--store",
                str(project / ".sldb"),
                "--pythonpath",
                repo_pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()

    monkeypatch.chdir(project)
    assert (
        cli_main(
            [
                "inbox",
                "Track this inbox note automatically.",
                "--title",
                "auto track inbox",
                "--pythonpath",
                repo_pythonpath,
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "Tracked '" in out

    store = project / ".sldb"
    entry = next(m for m in load_store_index(store).models if m.name == "InboxNoteDoc")
    model_index = load_models_index(project / entry.models_index)
    docs_index = load_documents_index(project / model_index.documents_index)
    tracked = next(doc for doc in docs_index.documents if "auto-track-inbox" in doc.name)
    assert tracked.path.startswith("desk/inbox/")


def test_explore_searches_docs_and_docstrings(tmp_path, capsys):
    docs_root = tmp_path / "docs"
    code_root = tmp_path / "src"
    docs_root.mkdir()
    code_root.mkdir()

    (docs_root / "faq.md").write_text(
        "# FAQ\n\nThe store keeps metadata close to Markdown.\n",
        encoding="utf-8",
    )
    (code_root / "knowledge.py").write_text(
        '"""Store helpers for SLDB docs."""\n\n\nclass Guide:\n    """StructuredNLDoc-oriented guide surface."""\n',
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "explore",
                "store",
                "--docs-root",
                str(docs_root),
                "--code-root",
                str(code_root),
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)["results"]
    assert any(item["source"] == "docs" for item in payload)
    assert any(item["source"] == "docstrings" for item in payload)

    assert (
        cli_main(
            [
                "docs",
                "explore",
                "StructuredNLDoc",
                "--source",
                "docstrings",
                "--docs-root",
                str(docs_root),
                "--code-root",
                str(code_root),
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)["results"]
    assert payload[0]["source"] == "docstrings"
    assert payload[0]["anchor"] == "Guide"


def test_ast_show_document_has_sections(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "ast",
                "show",
                "docs/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["document"]["name"] == "roadmap"
    titles = [section["title"] for section in payload["document"]["sections"]]
    assert "Tasks" in titles
    assert payload["document"]["ir"]["context"]["physical"]["path"] == "roadmap.md"
    assert payload["document"]["ir"]["structure"][0]["kind"] == "section"
    assert payload["document"]["ir"]["graph"]["edges"][0]["relation"] == "has_section"
    assert payload["document"]["ir"]["context_index"][0]["title"] == "Roadmap"
    assert (
        "type.documentation.Readme"
        in payload["document"]["ir"]["context_index"][1]["about"]
    )


def test_ast_show_field_nodes_have_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "ast",
                "show",
                "docs/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    nodes = payload["document"]["ir"]["nodes"]
    field_to_section = {node["field_path"]: node["owning_section"] for node in nodes}
    assert field_to_section["title"] == "roadmap"
    assert field_to_section["status"] == "roadmap"
    assert field_to_section["tasks"] == "roadmap/tasks"
    assert field_to_section["semantic_tags"] == "roadmap/semantic-tags"


def test_find_supports_physical_and_semantic(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "find",
                "roadmap",
                "--in",
                "physical",
                "--type",
                "doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    physical = json.loads(capsys.readouterr().out)["results"]
    assert physical[0]["doc"] == "roadmap"

    assert (
        cli_main(
            [
                "find",
                "type.documentation.Readme",
                "--in",
                "semantic",
                "--type",
                "doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    semantic = json.loads(capsys.readouterr().out)["results"]
    # Semantic index exposes the full sorted tag set: model semantics (base
    # representation/source defaults plus the declared type) union payload tags.
    assert semantic[0]["semantic_tags"] == [
        "project.sldb.database",
        "representation.markdown",
        "source.document.markdown",
        "type.documentation.Readme",
    ]


def test_models_template_edit_writes_draft_without_mutating_active_source(tmp_path):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    original = module_path.read_text(encoding="utf-8")
    template_path = _write_template(
        tmp_path / "updated.template.md",
        "# ⸢rev•title⸥\n\nSummary: active draft\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n",
    )

    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    draft_path = module_path.with_name(module_path.name + ".temp")
    assert draft_path.exists()
    assert "Summary: active draft" in draft_path.read_text(encoding="utf-8")
    assert module_path.read_text(encoding="utf-8") == original


def test_models_validate_promotes_valid_template_draft_and_reindexes(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    template_path = _write_template(
        tmp_path / "promote.template.md",
        "# ⸢rev•title⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n\n## Review\n\nReady for validation.\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert "validated draft" in capsys.readouterr().out
    assert "## Review" in module_path.read_text(encoding="utf-8")
    assert not module_path.with_name(module_path.name + ".temp").exists()

    capsys.readouterr()
    assert (
        cli_main(["stores", "check", "--store", str(store), "--pythonpath", pythonpath])
        == 0
    )


def test_models_validate_rejects_draft_with_unknown_field_reference(tmp_path):
    store, pythonpath = _setup_store(tmp_path)
    template_path = _write_template(
        tmp_path / "invalid.template.md",
        "# ⸢rev•title⸥\n\nMissing: ⸢rev•missing_field⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    with pytest.raises(SystemExit, match="references unknown fields: missing_field"):
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )


def test_models_fields_add_and_promote_bumps_model_version(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version

    assert (
        cli_main(
            [
                "models",
                "fields",
                "add",
                "RoadmapDoc",
                "summary",
                "--type",
                "str",
                "--description",
                "Short summary.",
                "--default",
                '"Pending review"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    template_path = _write_template(
        tmp_path / "field-add.template.md",
        "# ⸢rev•title⸥\n\nSummary: ⸢rev•summary⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n\n## Semantic Tags\n\n- ⸢rev,list•semantic_tags⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    after = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert after == before + 1
    active_source = module_path.read_text(encoding="utf-8")
    assert (
        "summary: str = Field(default='Pending review', description='Short summary.')"
        in active_source
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "show",
                "RoadmapDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert f"version: {after}" in capsys.readouterr().out


def test_models_fields_remove_requires_existing_field_and_bumps_version(
    tmp_path, capsys
):
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"

    with pytest.raises(SystemExit, match="Field 'missing' does not exist"):
        cli_main(
            [
                "models",
                "fields",
                "remove",
                "RoadmapDoc",
                "missing",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )

    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert (
        cli_main(
            [
                "models",
                "fields",
                "remove",
                "RoadmapDoc",
                "semantic_tags",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    template_path = _write_template(
        tmp_path / "field-remove.template.md",
        "# ⸢rev•title⸥\n\nStatus: ⸢rev•status⸥\n\n## Tasks\n\n- ⸢rev,list•tasks⸥\n",
    )
    assert (
        cli_main(
            [
                "models",
                "template",
                "edit",
                "RoadmapDoc",
                "--input",
                str(template_path),
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(
            [
                "models",
                "validate",
                "RoadmapDoc",
                "--promote",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    after = load_models_index(_model_index_path(store, "RoadmapDoc")).version
    assert after == before + 1
    active_source = module_path.read_text(encoding="utf-8")
    assert "semantic_tags:" not in active_source


def test_find_section_where_predicates(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(
            [
                "find",
                "tasks",
                "--type",
                "section",
                "--where",
                '"Tasks" in about',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    titles = [r["title"] for r in results]
    assert "Tasks" in titles

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"Semantic Tags" in about',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Semantic Tags"

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"Roadmap" in breadcrumbs',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) > 1
    for r in results:
        assert "Roadmap" in r.get("breadcrumbs", [])

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                '"type.documentation.Readme" in semantic_tags',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) == 3

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                'path = "roadmap.md#roadmap"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Roadmap"

    assert (
        cli_main(
            [
                "find",
                "",
                "--type",
                "section",
                "--where",
                'path = "roadmap.md#roadmap/tasks"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Tasks"


def test_fields_update_append_and_clean(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    target = "docs/roadmap/tasks"
    assert (
        cli_main(
            [
                "fields",
                "append",
                target,
                '"Ship CLI"',
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
                "fields",
                "clean",
                target,
                "--dedupe",
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
                "fields",
                "update",
                "docs/roadmap/status",
                '"accepted"',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "show",
                "docs/roadmap/status",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    status = json.loads(capsys.readouterr().out)
    assert status["value"] == "accepted"

    assert (
        cli_main(
            [
                "fields",
                "show",
                target,
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    tasks = json.loads(capsys.readouterr().out)["value"]
    assert tasks == ["Ship CLI", "Write docs"]


def test_fields_update_can_clear_list_field(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "update",
                "docs/roadmap/tasks",
                "[]",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "show",
                "docs/roadmap/tasks",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    value = json.loads(capsys.readouterr().out)
    assert value["value"] == []


def test_models_create_stdout(tmp_path, capsys):
    template = tmp_path / "template.md"
    template.write_text("# ⸢rev•title⸥\n", encoding="utf-8")
    fields = tmp_path / "fields.yaml"
    fields.write_text(
        """
fields:
  - name: title
    type: str
    description: Document title.
""".strip()
        + "\n",
        encoding="utf-8",
    )
    assert (
        cli_main(
            [
                "models",
                "create",
                "GeneratedDoc",
                "--template",
                str(template),
                "--fields",
                str(fields),
                "--stdout",
            ]
        )
        == 0
    )
    out = capsys.readouterr().out
    assert "class GeneratedDoc(StructuredNLDoc):" in out
    assert "title: str = Field(description=" in out
    assert "Document title." in out


def test_sections_show_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    titles = [entry["title"] for entry in payload["sections"]]
    assert "Roadmap" in titles
    assert "Tasks" in titles
    assert "Semantic Tags" in titles


def test_sections_find_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "find",
                "tasks",
                "--in",
                "semantic",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["title"] == "Tasks"

    assert (
        cli_main(
            [
                "sections",
                "find",
                "",
                "--where",
                '"Roadmap" in breadcrumbs',
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert len(results) >= 2


def test_sections_fields_command(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "sections",
                "fields",
                "docs/roadmap/roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    fields = json.loads(capsys.readouterr().out)["fields"]
    field_paths = [f["field_path"] for f in fields]
    assert "title" in field_paths
    assert "status" in field_paths

    assert (
        cli_main(
            [
                "sections",
                "fields",
                "docs/roadmap/roadmap/tasks",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    fields = json.loads(capsys.readouterr().out)["fields"]
    field_paths = [f["field_path"] for f in fields]
    assert "tasks" in field_paths


def test_field_query_includes_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "fields",
                "query",
                "title",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["owning_section"] == "roadmap"


def test_sections_show_identical_with_and_without_persisted_index(tmp_path, capsys):
    """Read-side commands produce identical section output with or without persisted index."""
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()

    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    before = json.loads(capsys.readouterr().out)

    assert (
        cli_main(
            ["stores", "update", "--store", str(store), "--pythonpath", pythonpath]
        )
        == 0
    )
    capsys.readouterr()

    assert (
        cli_main(
            [
                "sections",
                "show",
                "roadmap",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    after = json.loads(capsys.readouterr().out)

    before_sections = before.get("sections", [])
    after_sections = after.get("sections", [])
    assert len(before_sections) == len(after_sections)
    for b, a in zip(before_sections, after_sections):
        assert b["title"] == a["title"]
        assert b["path"] == a["path"]
        assert b["breadcrumbs"] == a["breadcrumbs"]
        assert b["about"] == a["about"]


def test_find_field_shows_owning_section(tmp_path, capsys):
    store, pythonpath = _setup_store(tmp_path)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "find",
                "title",
                "--type",
                "field",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
                "--format",
                "json",
            ]
        )
        == 0
    )
    results = json.loads(capsys.readouterr().out)["results"]
    assert results[0]["owning_section"] == "roadmap"


def _add_summary_draft(store: Path, pythonpath: str) -> None:
    assert (
        cli_main(
            [
                "models", "fields", "add", "RoadmapDoc", "summary",
                "--type", "str", "--description", "Short summary.", "--default", '"Pending review"',
                "--store", str(store), "--pythonpath", pythonpath,
            ]
        )
        == 0
    )


@pytest.mark.parametrize(
    "failing",
    [
        "resolve_model_ref",         # pre-write: model resolution
        "rehash_documents",          # pre-write: document hash pass
        "save_documents_index",      # mid-write: docs index written
        "save_models_index",         # mid-write: models index written
        "documents_hash.invalidate", # post-write: derived cache invalidation
        "rebuild_derived_indexes",   # post-write: derived index rebuild
        "cascade_store_hash",            # post-write: hash_a cascade
    ],
)
def test_models_promote_failure_restores_model_draft_and_indexes(tmp_path, monkeypatch, failing):
    """A promote whose reindex fails leaves the store as it was: active model, draft and indexes intact.

    Promote dispatches to the real ``models update`` route (``ModelsCLI`` -> ``ModelCLI.update`` in
    `sldb.cli.commands.model`), so the failure is injected on a module-level name that route actually
    calls - never on `sldb.cli.commands.model_update`, which the route does not import. Each param is
    a distinct stage of that route; all must land inside ``restored_on_failure``.
    """
    store, pythonpath = _setup_store(tmp_path)
    module_path = Path(pythonpath) / "cli_v2_models.py"
    draft_path = module_path.with_name(module_path.name + ".temp")
    _add_summary_draft(store, pythonpath)
    original, draft = module_path.read_text(encoding="utf-8"), draft_path.read_text(encoding="utf-8")
    before = load_models_index(_model_index_path(store, "RoadmapDoc")).version

    def boom(*args, **kwargs):
        raise RuntimeError("reindex failed")

    monkeypatch.setattr(f"sldb.cli.commands.model.{failing}", boom)
    with pytest.raises((SystemExit, RuntimeError)):
        cli_main(["models", "validate", "RoadmapDoc", "--promote", "--store", str(store), "--pythonpath", pythonpath])
    monkeypatch.undo()

    assert module_path.read_text(encoding="utf-8") == original
    assert draft_path.read_text(encoding="utf-8") == draft
    assert load_models_index(_model_index_path(store, "RoadmapDoc")).version == before
    assert cli_main(["stores", "check", "--store", str(store), "--pythonpath", pythonpath]) == 0


def test_models_promote_json_output_is_pure_json(tmp_path, capsys):
    """--format json keeps stdout parseable: update's progress line must not precede the report."""
    store, pythonpath = _setup_store(tmp_path)
    _add_summary_draft(store, pythonpath)
    capsys.readouterr()
    assert (
        cli_main(
            [
                "models", "validate", "RoadmapDoc", "--promote", "--format", "json",
                "--store", str(store), "--pythonpath", pythonpath,
            ]
        )
        == 0
    )
    report = json.loads(capsys.readouterr().out)
    assert report["promoted"] is True and report["draft"] is True

FILE:instruccion
Cold-bundle de la tarea task-sldb-version-dice-qué-commit-corre-versión-del-paquete-más-git-describe-del-checkout-editable: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_envelope.py
- PYTHONPATH=src python -m sldb --version


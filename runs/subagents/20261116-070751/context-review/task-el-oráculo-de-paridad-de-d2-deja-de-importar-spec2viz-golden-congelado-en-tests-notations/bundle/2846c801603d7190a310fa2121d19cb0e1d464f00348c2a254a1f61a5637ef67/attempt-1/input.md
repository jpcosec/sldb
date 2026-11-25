FILE:desk/tasks/task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations.md
---
sldb:
  by: agent
  at: '2026-11-16T06:18:23Z'
  authority: generated
  via: save_document_payload
id: task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md
depends_on: []
pills: []
files:
- tests/notations/test_component_spec_python.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El oráculo de paridad de D2 deja de importar spec2viz: golden congelado en tests/notations

## Rationale

_Explain why this task exists or the business driver behind it._

IR13 (gate de retiro de spec2viz) pide migrar lo que queda de sldb sobre spec2viz. Los puntos 2 y 3 (vistas.yml e identity.toml) ya los cubre la tarea task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con. Queda el punto 1: tests/notations/test_component_spec_python.py:43 hace pytest.importorskip("spec2viz.generators.python_ast") y compara en vivo con spec2viz; sin spec2viz instalado el test se salta y la paridad deja de comprobarse. Origen: desk/inbox/20261115-224828-suggestion-ir13-pide-migrar-lo-que-queda-de-sldb-sobre-spec2viz-or-culo-de-d2-vistas-yml-identity-toml.md.

## Goal

_Describe the concrete result this task must produce._

La comparación de paridad corre siempre contra un golden versionado en tests/ y el archivo de test no importa spec2viz en ninguna rama.

## Scope

_State what is in scope and what is out of scope._

Entra: generar una sola vez, con spec2viz instalado, la salida de spec2viz.generators.python_ast para la entrada que hoy usa el test y guardarla como golden en el golden nuevo component_spec_python_spec2viz.json en la carpeta goldens de tests/notations (JSON con sort_keys=True e indent=2), con la clave "_source" que dice el commit de spec2viz del que salió; cambiar el test para comparar con ese golden; quitar el importorskip. Si spec2viz no está instalado en la máquina, generar el golden desde el checkout /mnt/ssd/proyectos/SLDB_1/spec2viz con PYTHONPATH, sin instalarlo. CHANGELOG.md. No entra: vistas.yml, identity.toml ni otros usos de spec2viz (tarea task-los-specs-de-docs-architecture-...), y cambiar component_spec_from_python (si la paridad falla con el golden, se reporta, no se ajusta el golden a mano).

Precisiones (preflight-1): la entrada es el árbol TREE y la fixture tree de tests/notations/test_component_spec_python.py, y la comparación viva es test_matches_spec2viz_on_modules_classes_and_defines, que compara _defined(spec) con _defined(python_ast.generate_python_ast_spec(tree)). El golden es un JSON con tres claves: "modules" y "classes" (los dos dicts de _defined) y "defines" (la lista ordenada de pares [from, to]), más "_source": la salida de `git -C /mnt/ssd/proyectos/SLDB_1/spec2viz rev-parse HEAD`. Se genera una vez con `PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/spec2viz` sobre una copia de TREE escrita en un directorio temporal; la carpeta goldens se crea dentro de tests/notations. El test pasa a leer el golden y comparar contra _defined(spec) convertido a la misma forma. La comprobación "sin spec2viz" es: `python -c "import spec2viz"` falla en el entorno de la suite, o bien correr el test con PYTHONPATH=src y sin el checkout de spec2viz en sys.path. Solo se compara lo que hoy compara el test (módulos, clases, defines), no imports.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/notations/test_component_spec_python.py, en especial la línea 43 y la función que compara. 2) Correr una vez el generador de spec2viz sobre la misma entrada y guardar su salida normalizada como golden. 3) Reemplazar la comparación viva por la lectura del golden. 4) grep -n spec2viz tests/notations/test_component_spec_python.py no devuelve imports. 5) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- ! grep -n 'import.*spec2viz\|importorskip("spec2viz' tests/notations/test_component_spec_python.py

## Done When

_Name the observable condition that makes the task complete._

El test pasa sin spec2viz importable (comprobado con python -c "import spec2viz" fallando o con PYTHONPATH sin spec2viz) y el grep de Validation no encuentra imports de spec2viz; golden y CHANGELOG commiteados.

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

FILE:tests/notations/test_component_spec_python.py
"""Component spec of a Python tree from `sldb.code.scan_tree` (`component_spec_from_python`).

spec2viz has no tests for its `python_ast` generator: the comparison test runs both on the same
small tree and asserts the same modules, classes and `defines` relations. Skipped without the
`[code]` extra (tree-sitter); the extra-missing alert is tested by simulating its absence.
"""
import pytest
import yaml

from sldb.api.notations import component_spec_from_python, validate_spec, write_component_spec
from sldb.cli import main
from sldb.code.runtime import available
from sldb.models.notation.diagram_specs.component import ComponentDiagram

needs_code = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

TREE = {
    "pkg/__init__.py": "",
    "pkg/a.py": "import os\nimport json, sys as s\nfrom pkg.sub import b\nfrom . import c\nfrom .sub.b import Thing\n"
                "class A:\n    class Inner: pass\n    def m(self): pass\nif True:\n    class Hidden: pass\ndef f(): pass\nclass Z: pass\n",
    "pkg/sub/b.py": "from __future__ import annotations\nfrom pkg.a import A\nclass Thing(A): pass\n",
    "pkg/bad.py": "class Ok: pass\ndef broken(:\n",
    "other/x.py": "class X: pass\n",
}


@pytest.fixture
def tree(tmp_path):
    for rel, text in TREE.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    return tmp_path


def _defined(spec: dict) -> tuple[dict, dict, set]:
    nodes = spec["data"]["nodes"]
    pick = lambda kind: {k: v["label"] for k, v in nodes.items() if v["kind"] == kind}  # noqa: E731
    return pick("module"), pick("class"), {(e["from"], e["to"]) for e in spec["data"]["edges"] if e["relation"] == "defines"}


@needs_code
def test_matches_spec2viz_on_modules_classes_and_defines(tree):
    python_ast = pytest.importorskip("spec2viz.generators.python_ast")
    spec, findings = component_spec_from_python(tree)
    validate_spec(ComponentDiagram.model_validate(spec))
    assert _defined(spec) == _defined(python_ast.generate_python_ast_spec(tree))
    assert _defined(spec)[1] == {"class_pkg_a_A": "A", "class_pkg_a_Z": "Z", "class_pkg_sub_b_Thing": "Thing", "class_other_x_X": "X"}
    assert [(f.level, f.code, f.subject) for f in findings] == [("alert", "component-spec/syntax-error", "pkg/bad.py")]


@needs_code
def test_imports_are_resolved_and_undeclared_targets_are_external(tree):
    spec, _ = component_spec_from_python(tree, project_id="p", title="P", root_package="pkg")
    imports = {(e["from"], e["to"]) for e in spec["data"]["edges"] if e["relation"] == "imports"}
    assert ("module_pkg_a", "module_pkg_sub_b") in imports  # `from .sub.b import Thing`, relativo resuelto
    assert {("module_pkg_a", "module_os"), ("module_pkg_a", "module_json"), ("module_pkg_a", "module_sys")} <= imports
    assert spec["data"]["nodes"]["module_os"] == {"label": "os", "kind": "external"}
    assert "module_other_x" not in spec["data"]["nodes"] and spec["id"] == "p"
    validate_spec(ComponentDiagram.model_validate(spec))


@needs_code
def test_write_component_spec_and_cli_python(tree, tmp_path, capsys):
    out = tmp_path / "out" / "arch.yml"
    assert main(["notations", "from-graph", "--python", str(tree), "--id", "arch", "--output", str(out)]) == 0
    assert "Generated" in capsys.readouterr().out
    spec, _ = component_spec_from_python(tree, project_id="arch", title="arch AST Architecture")
    assert yaml.safe_load(out.read_text(encoding="utf-8")) == spec
    write_component_spec(spec, tmp_path / "again.yml")
    assert (tmp_path / "again.yml").read_text(encoding="utf-8") == out.read_text(encoding="utf-8")


def test_without_code_extra_returns_the_alert_and_writes_nothing(tree, tmp_path, monkeypatch, capsys):
    import sldb.api.notations.component_spec_python as gen

    monkeypatch.setattr(gen, "available", lambda: False)
    spec, findings = component_spec_from_python(tree)
    assert spec is None
    assert [f.as_dict() for f in findings] == [{"level": "alert", "code": "component-spec/code-extra-missing", "subject": str(tree),
                                                "what": "no hay tree-sitter", "fix": "pip install 'structuredLanguageDB[code]'", "document": None}]
    assert main(["notations", "from-graph", "--python", str(tree), "--output", str(tmp_path / "x.yml")]) == 1
    assert "component-spec/code-extra-missing" in capsys.readouterr().err and not (tmp_path / "x.yml").exists()

FILE:instruccion
Cold-bundle de la tarea task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py
- ! grep -n 'import.*spec2viz\|importorskip("spec2viz' tests/notations/test_component_spec_python.py


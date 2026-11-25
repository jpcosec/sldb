FILE:desk/tasks/task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains.md
---
sldb:
  by: agent
  at: '2026-11-16T06:18:43Z'
  authority: generated
  via: save_document_payload
id: task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-test-where-retired-de-go10-confunde-la-relación-contains-con-el-operador-viejo.md
depends_on: []
pills: []
files:
- tests/store/test_where_retired.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# test_where_retired distingue el operador viejo contains de la relación de aristas contains

## Rationale

_Explain why this task exists or the business driver behind it._

tests/store/test_where_retired.py::test_no_old_operator_in_the_code_of_docs (aceptación de GO10, 1e6ecd55) busca los ocho operadores viejos del lenguaje de consultas (eq, ne, gt, lt, contains, starts_with, is_null, is_not_null) como palabra entera en todo bloque o span de código de docs/. Pero contains también es el nombre de la relación de aristas de contención (__containment__, sldb edges). Un doc que nombra esa relación entre comillas invertidas hace fallar la suite aunque no hable del lenguaje viejo; pasó con tres docs y se tapó en c2d279d0 quitando las comillas. Origen: nota del inbox desk/inbox/inbox-note-test-where-retired-de-go10-confunde-la-relación-contains-con-el-operador-viejo.md.

## Goal

_Describe the concrete result this task must produce._

El test sigue fallando cuando un bloque o span de código de docs/ usa un operador viejo como operador de predicado, y deja de fallar cuando contains aparece solo como nombre de la relación de aristas.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar tests/store/test_where_retired.py y agregar una línea en CHANGELOG.md bajo el encabezado de la versión sin publicar ("test_where_retired ya no confunde la relación contains con el operador viejo"). Regla exacta: los siete operadores eq, ne, gt, lt, starts_with, is_null, is_not_null se siguen contando como hoy (palabra entera en código de docs/). contains se cuenta como operador viejo solo si casa el patrón PREDICATE_CONTAINS = re.compile(r"(?<![\w.])[A-Za-z_][\w.]*\s+contains\s+(\"|\x27|\d|\[|[A-Za-z_])|(?<!\w)contains\s*:"), es decir: un identificador de campo (letras, dígitos, guion bajo y puntos, como status o a.b) seguido de espacios, contains, espacios y el inicio de un valor (comilla, dígito, corchete o identificador), o la forma contains: (clave de un mapeo de operadores). contains solo, entre comillas invertidas o como argumento de una opción (--relation contains) no cuenta. Dos tests nuevos en el mismo archivo, sobre texto en memoria: test_contains_as_edge_relation_is_not_an_old_operator (los textos "contains", "sldb edges --relation contains" y "la relación contains" dan cero operadores) y test_contains_as_predicate_is_an_old_operator ("status contains \"x\"" y "contains: foo" dan contains). Si docs/ actual ya tiene otro operador viejo y el test falla por eso, no se toca docs/: se reporta el archivo y la línea en el informe del ejecutor y la tarea queda bloqueada. No entra: tocar docs/ ni src/, cambiar la excepción de la tabla Histórico de docs/architecture/rules-language.md, ni cambiar el test de identificadores where_parse/FieldCondition.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/store/test_where_retired.py completo (OPERATORS en la línea 18, INLINE, _code, _historic_rows y test_no_old_operator_in_the_code_of_docs). 2) Quitar contains de OPERATORS y agregar la constante PREDICATE_CONTAINS con el regex exacto de Scope. 3) Agregar la función pura _old_operators(code: str) -> list[str] que devuelve los operadores viejos encontrados en un fragmento de código (los de OPERATORS más "contains" cuando casa PREDICATE_CONTAINS), y hacer que test_no_old_operator_in_the_code_of_docs la use. 4) Agregar los dos tests nuevos, que llaman a _old_operators directamente. 5) Correr el archivo. 6) Línea en CHANGELOG.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py

## Done When

_Name the observable condition that makes the task complete._

TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py pasa con los dos tests nuevos; _old_operators("sldb edges --relation contains") == [] y _old_operators("status contains \"x\"") == ["contains"]; git diff --stat del commit muestra solo tests/store/test_where_retired.py y CHANGELOG.md.

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

FILE:tests/store/test_where_retired.py
"""GO10: the old query languages are gone from `src/` and `docs/` (rules-language.md §7).

Two greps, as the acceptance fixes them. The identifiers `where_parse` and `FieldCondition`
(substrings, prose included: they are code names) appear nowhere in `src/` or `docs/`; the
eight old operator names, as whole words, appear in no fenced block or inline code span of a
Markdown file of `docs/`. The one exception is the rows of the historical equivalence table of
`docs/architecture/rules-language.md`, under a heading that says "Histórico".
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORIC_DOC = ROOT / "docs" / "architecture" / "rules-language.md"
IDENTIFIERS = re.compile(r"where_parse|FieldCondition")
OPERATORS = re.compile(r"(?<!\w)(eq|ne|gt|lt|contains|starts_with|is_null|is_not_null)(?!\w)")
INLINE = re.compile(r"(`+)(.+?)\1", re.S)
HEADING = re.compile(r"^(#{1,6})\s")


def _historic_rows(path: Path, lines: list[str]) -> set[int]:
    """Line numbers of the table rows under the "Histórico" heading (only in the one doc)."""
    if path != HISTORIC_DOC:
        return set()
    rows, level = set(), None
    for number, line in enumerate(lines, 1):
        heading = HEADING.match(line)
        if heading:
            depth = len(heading.group(1))
            if level is not None and depth <= level:
                level = None
            if re.search(r"Hist[óo]rico", line):
                level = depth
        elif level is not None and line.lstrip().startswith("|"):
            rows.add(number)
    return rows


def _code(lines: list[str]) -> list[tuple[int, str]]:
    """`(line number, code)` for every fenced line and every inline code span."""
    found, fence, paragraph = [], None, []

    def flush() -> None:
        if paragraph:
            first, text = paragraph[0][0], "\n".join(line for _, line in paragraph)
            found.extend((first + text.count("\n", 0, m.start()), m.group(2)) for m in INLINE.finditer(text))
            paragraph.clear()

    for number, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if fence:
            fence = None if stripped.startswith(fence) else fence
            if fence:
                found.append((number, line))
        elif stripped.startswith(("```", "~~~")):
            flush()
            fence = stripped[:3]
        elif not stripped:
            flush()
        else:
            paragraph.append((number, line))
    flush()
    return found


def _files(*folders: str):
    for folder in folders:
        yield from (p for p in sorted((ROOT / folder).rglob("*")) if p.is_file() and "__pycache__" not in p.parts)


def test_no_old_identifier_in_src_or_docs():
    hits = []
    for path in _files("src", "docs"):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        historic = _historic_rows(path, lines)
        hits += [f"{path.relative_to(ROOT)}:{n}" for n, line in enumerate(lines, 1) if IDENTIFIERS.search(line) and n not in historic]
    assert hits == []


def test_no_old_operator_in_the_code_of_docs():
    hits = []
    for path in (p for p in _files("docs") if p.suffix == ".md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        historic = _historic_rows(path, lines)
        hits += [f"{path.relative_to(ROOT)}:{n}: {m.group(1)}" for n, code in _code(lines) if n not in historic for m in OPERATORS.finditer(code)]
    assert hits == []

FILE:instruccion
Cold-bundle de la tarea task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py


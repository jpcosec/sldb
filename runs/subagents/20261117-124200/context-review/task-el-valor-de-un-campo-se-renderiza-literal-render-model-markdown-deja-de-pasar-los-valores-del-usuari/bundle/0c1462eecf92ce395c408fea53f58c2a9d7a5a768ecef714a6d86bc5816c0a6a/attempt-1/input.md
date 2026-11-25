FILE:desk/tasks/task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari.md
---
sldb:
  by: agent
  at: '2026-11-17T05:09:24Z'
  authority: generated
  via: create_document
id: task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md
depends_on: []
pills: []
files:
- src/sldb/core/renderer_engine/base.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El valor de un campo se renderiza literal: render_model_markdown deja de pasar los valores del usuario por Jinja

## Rationale

_Explain why this task exists or the business driver behind it._

render_model_markdown interpreta como Jinja el valor de un campo de texto: src/sldb/core/renderer_engine/base.py (BaseRenderer.replace_markers) sustituye los valores de los marcadores dentro del texto fuente del bloque y después compila todo con jinja_env.from_string(source).render(**data). Dos o tres llaves de apertura seguidas rompen el render con TemplateSyntaxError; una expresión Jinja válida se evalúa y se guarda alterada (7*7 entre llaves dobles se guarda como 49; un comentario Jinja desaparece) con rc 0. Le pasa a deskops en edit task y message send. Es una inyección de plantilla con datos del usuario. Origen: desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md.

## Goal

_Describe the concrete result this task must produce._

El valor de un campo se guarda literal, byte a byte, y vuelve igual en extract; solo la plantilla del modelo es Jinja. Ningún valor con llaves, porcentajes o almohadillas cambia el render ni lo rompe.

## Scope

_State what is in scope and what is out of scope._

Entra: separar en replace_markers lo que es plantilla de lo que es dato: los valores de los marcadores no llegan a Jinja como código (por ejemplo, sustituirlos por variables de Jinja o por tokens que se reemplazan después del render, o escapar el valor con raw); mantener el comportamiento de optrev y de las líneas ausentes; tests de roundtrip con valores que contengan dos y tres llaves de apertura, una expresión, un comentario Jinja, bloques de control y llaves de cierre, en un archivo de tests del renderer existente. CHANGELOG. No entra: cambiar la sintaxis de las plantillas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/core/renderer_engine/base.py y sus subclases, y quién llama a replace_markers. 2) Reproducir los casos de la nota con un modelo de prueba. 3) Implementar la separación. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos de roundtrip; los casos de la nota se guardan literales; CHANGELOG y commit; aviso a deskops para que quite su xfail.

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

FILE:src/sldb/core/renderer_engine/base.py
from __future__ import annotations

import re
from typing import Any

import yaml
from jinja2 import Environment

from sldb.core.handlers.utils import parse_marker
from sldb.core.renderer_engine.jinja_trailing import unshield_trailing_newline
from sldb.core.renderer_engine.python_expr import PythonExpressionRenderer
from sldb.core.renderer_engine.table_markdown import format_table_cell, is_table_marker, render_markdown_table, table_columns


class BaseRenderer:
    """
    Base class for rendering components.
    """

    def __init__(self, jinja_env: Environment, recorder: Any = None):
        self.jinja_env = jinja_env
        self.py_renderer = PythonExpressionRenderer()
        self.recorder = recorder

    def replace_markers(self, text: str, data: dict[str, Any]) -> str:
        lines = []
        for line in text.split("\n"):
            if self._is_absent_optional_line(line, data):
                continue
            lines.append(re.sub(r"⸢([^⸥]+)⸥", lambda m: self._sub_marker(m, data), line))
        source = "\n".join(lines)
        if self.recorder is not None:
            source = unshield_trailing_newline(source)
        return self.jinja_env.from_string(source).render(**data)

    def _is_absent_optional_line(self, line: str, data: dict[str, Any]) -> bool:
        """An optrev marker whose value is None leaves NO trace in the render:
        its whole line is dropped, so the document reads byte-for-byte as if
        the field were never declared (contract: 'It MAY BE ABSENT in the
        document'). Only two shapes qualify: `key: ⸢optrev•key⸥` or
        `⸢optrev•key⸥` alone on the line (leading whitespace allowed).

        A line that SHARES its content with anything else -- a table row of
        cells, a list bullet, preceding text, another marker -- is never
        dropped; there the marker is replaced with the empty string (today's
        behavior) because deleting the line would corrupt the surrounding
        structure (a table would lose a column, a list item would vanish).
        An empty list/dict VALUE (`[]`/`{}`) is not None, so it still renders
        (as an empty table or empty mapping); only a None value means absent.

        kind == 'render' markers are NOT optional-extractable fields: they
        keep their historical empty-string behavior and are never the reason
        a line is omitted.
        """
        m = re.match(r"^\s*(?:[A-Za-z0-9_-]+\s*:\s*)?⸢([^⸥]+)⸥\s*$", line)
        if not m:
            return False
        marker = parse_marker(m.group(1))
        if not marker.is_optional:
            return False
        return data.get(marker.name) is None

    def _sub_marker(self, match: re.Match, data: dict[str, Any]) -> str:
        m = parse_marker(match.group(1))
        out = self._resolve_marker(m, match, data)
        if self.recorder is None or out == match.group(0):
            return out
        return self.recorder.wrap(out, self.recorder.meta_for(m))

    def _resolve_marker(self, m: Any, match: re.Match, data: dict[str, Any]) -> str:
        """The rendered surface of one marker, or the literal marker when unresolved.

        Args:
            m: The parsed marker.
            match: The regex match of the marker in the template line.
            data: The payload the marker reads from.

        Returns:
            The value's text, an empty string for an absent optional, or the
            literal marker when the value is missing and required.
        """
        if m.kind == "py": return self.py_renderer.render(m.name, data, match.group(0))
        val = data.get(m.name)
        if val is None: return "" if m.is_optional or m.kind == "render" else match.group(0)
        if is_table_marker(m): return render_markdown_table(val, table_columns(m, val))
        return self._format_value(val, m)

    def _format_value(self, val: Any, marker: Any) -> str:
        if "dict" in marker.traits or isinstance(val, (dict, list)):
            if "list" in marker.traits and not isinstance(val, (dict, list)): return str(val)
            return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()
        return str(val)

    _is_table_marker = staticmethod(is_table_marker)
    _table_columns = staticmethod(table_columns)
    _render_markdown_table = staticmethod(render_markdown_table)
    _format_table_cell = staticmethod(format_table_cell)

    def get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        """Helper to get node source from block text."""
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])

FILE:instruccion
Cold-bundle de la tarea task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast


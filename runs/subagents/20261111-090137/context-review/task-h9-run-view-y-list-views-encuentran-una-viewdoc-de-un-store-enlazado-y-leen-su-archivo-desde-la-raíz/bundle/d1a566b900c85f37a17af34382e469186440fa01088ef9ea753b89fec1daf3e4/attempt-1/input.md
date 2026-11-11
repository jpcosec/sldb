FILE:desk/tasks/task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz.md
---
sldb:
  by: agent
  at: '2026-11-11T09:00:54Z'
  authority: generated
  via: create_document
id: task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/views/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-h9-run-view-no-encuentra-una-viewdoc-de-un-store-enlazado-unknown-view-bloquea-cc34-de-deskops-da4.md
---

# H9: run_view y list_views encuentran una ViewDoc de un store enlazado y leen su archivo desde la raíz de ese store

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión del coordinador (DA4 -> B, 2026-11-11), prioridad detrás de seguridad. Las ViewDoc de deskops viven solo en el paquete (DA4, del dueño) y un desk las encuentra por el store enlazado; hoy run_view da Unknown view en todo store que solo enlaza.

## Goal

_Describe the concrete result this task must produce._

run_view, list_views y sldb serve encuentran una ViewDoc de un store enlazado, la leen desde la raíz de ese store por la guarda de lectura y la evalúan sobre el store que llama.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/views/, tests/api/, docs/, CHANGELOG.md. Fuera: la forma del resultado de run_view y los agregados de deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del coordinador (DA4 -> B, 2026-11-11): las ViewDoc de deskops viven solo como semillas del paquete (DA4, decisión del dueño), y un desk las encuentra por el store de deskops enlazado. Prioridad justo detrás de la tarea de seguridad live_stale. Desbloquea CC34 de deskops en los desks que no son el repo deskops.

REPORTE (worker de CC34, sldb 1c3132aa; nota de inbox 5ac79287): run_view (y por lo tanto sldb serve GET /views/<x>) sobre un store A que enlaza a un store B que trackea la ViewDoc da 'Unknown view'.

CAUSA (src/sldb/api/views/list_views.py):
- load_view busca f"{VIEW_MODEL}:{name}" en el índice, pero el índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' (por ejemplo 'lib:ViewDoc:board').
- read_view resuelve node.semantics['path'] contra open_store(store_path).project_root, el root del store LOCAL, no el del store enlazado que trackea la ViewDoc.
- list_views compone el índice con include_linked=False, así que tampoco lista las enlazadas.

ARREGLO (v1-v5):
v1 (resolución): load_view busca primero la ViewDoc local ('ViewDoc:<name>'). Si no hay, busca una enlazada ('<link>:ViewDoc:<name>'). Si hay más de una enlazada con el mismo nombre, el error las nombra (ambigua); no elige una.
v2 (archivo): read_view lee el archivo desde el project_root del store que trackea la ViewDoc (el enlazado, para un nodo enlazado). Lee por la guarda de lectura de la tarea de seguridad (sldb.store.source_read: dentro de la raíz de ese store, sin symlinks) si ya está en main; si no, deja un TODO con la referencia a esa tarea. Hoy read_view hace .read_text() sin guarda.
v3 (list_views): lista también las ViewDoc enlazadas, con el nombre calificado cuando hay choque.
v4 (evaluación): la ViewDoc enlazada se evalúa sobre los documentos del store A (el que llama), no sobre los del store B.
v5 (tests, tests/api/): un store A que enlaza a B, con la ViewDoc solo en B. run_view(A, 'board') la encuentra, lee su archivo desde la raíz de B y la evalúa sobre los documentos de A. list_views(A) la lista. Con dos enlazados con el mismo nombre, el error nombra la ambigüedad. Una ViewDoc local gana sobre una enlazada.

VALIDACIÓN: los 7 pasos del workflow de sldb los corre el coordinador. El worker corre los tests que toca, tests/api de views y test_clean_code_rules (límites de 80 líneas efectivas por archivo y 10 de lógica por función; un archivo nuevo necesita eje en contracts/layers.toml).

## Validation

_List the checks required before this task can close._

- Test con store A que enlaza a B y la ViewDoc solo en B: run_view(A) la encuentra y evalúa sobre A
- list_views(A) la lista; ambigüedad nombrada; la local gana
- test_clean_code_rules y tests de views verdes
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

v1-v5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.

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

FILE:instruccion
Cold-bundle de la tarea task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test con store A que enlaza a B y la ViewDoc solo en B: run_view(A) la encuentra y evalúa sobre A
- list_views(A) la lista; ambigüedad nombrada; la local gana
- test_clean_code_rules y tests de views verdes
- 7 pasos del workflow de sldb en clon limpio


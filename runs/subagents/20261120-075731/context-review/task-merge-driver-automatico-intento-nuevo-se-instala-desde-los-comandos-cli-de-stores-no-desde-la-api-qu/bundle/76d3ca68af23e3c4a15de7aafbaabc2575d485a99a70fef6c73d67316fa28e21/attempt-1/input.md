FILE:desk/tasks/task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu.md
---
sldb:
  by: agent
  at: '2026-11-20T07:56:29Z'
  authority: generated
  via: create_document
id: task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu
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
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Merge driver automático, intento nuevo: se instala desde los comandos CLI de stores, no desde la API que usan las transacciones

## Rationale

_Explain why this task exists or the business driver behind it._

Sigue a task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta, que agotó sus dos intentos. Intento 1 (68d4ee1d, revertido en 8e24da2e): instalaba el driver desde build_store/init_store/scaffold_store de la API, y rompía tests/test_transaction.py::test_split_restores_source_and_store_when_the_second_atom_create_fails de deskops, porque un build dentro de una Transaction escribe .gitattributes y git config fuera del rollback. Intento 2 (sin commit; patch en runs/subagents/exec-deskops-e-7b45b951426a-a2/intento2-sin-commit.patch): movió la instalación a los comandos CLI (bien, el test de deskops pasa), pero 3 de 9 tests de tests/api/test_gitignore_policy.py fallan porque los repos preparados con la API init_store() reciben ahora el alert merge-driver-missing y esos tests esperaban alerts vacíos.

## Goal

_Describe the concrete result this task must produce._

(1) 'sldb stores init', 'sldb stores scaffold' y 'sldb stores build' (los comandos de src/sldb/cli/commands/) instalan el merge driver cuando el store está en un repo git, con ensure_merge_driver/install_merge_driver: idempotente, sin nada fuera de git, y con aviso por stderr sin romper si git falla. Las funciones de API (init_store, scaffold_store, build_store) no lo instalan. (2) 'sldb stores check' da el alert stores/merge_driver_missing con el fix 'sldb stores merge-driver --install' cuando falta. (3) Los tests de tests/api/test_gitignore_policy.py que preparan un repo git con la API y comparan alerts esperan ahora también ese alert (es el comportamiento nuevo pedido). Si un test solo quiere aislar otra regla, que instale el driver antes o filtre por código, sin debilitar lo que verifica.

## Scope

_State what is in scope and what is out of scope._

Dentro: los tres comandos CLI, src/sldb/api/stores/ensure_merge_driver.py, store_surroundings.py, tests/store/test_merge_driver_auto_install.py, tests/api/test_gitignore_policy.py y los tests que haga falta ajustar por el alert nuevo, y CHANGELOG. Fuera: tocar init_store/scaffold_store/build_store de la API para que instalen nada.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: aplicar como punto de partida el patch del intento 2 (git apply runs/subagents/exec-deskops-e-7b45b951426a-a2/intento2-sin-commit.patch) y revisarlo contra el Goal. p2: correr tests/api/test_gitignore_policy.py y ajustar los 3 que fallan según el Goal (3). p3: correr también tests/store/test_merge_driver_auto_install.py, tests/store/test_stores_build.py, tests/api/test_scaffold_store.py, tests/api/test_api_stores.py y tests/test_clean_code_rules.py; y, si el contenedor tiene /workspace/deskops, el test de deskops 'tests/test_transaction.py -k second_atom_create_fails' con PYTHONPATH=/workspace/sldb/src. p4: bash tools/check.sh --fast: todas las puertas en verde salvo 'identidad' por workbench_demo (preexistente, excepción autorizada por el coordinador; decisión aparte). p5: COMMITEAR (git add de rutas nombradas, trailer Task-Id) y correr deskops advance. Una entrega sin commit es FALLA.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py tests/api/test_gitignore_policy.py

## Done When

_Name the observable condition that makes the task complete._

Los tests de p3 pasan; el commit existe con Task-Id; la suite completa de sldb la corre integrate y el integrador corre la de deskops.

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
Cold-bundle de la tarea task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/store/test_merge_driver_auto_install.py tests/api/test_gitignore_policy.py


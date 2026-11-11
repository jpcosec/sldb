FILE:desk/tasks/task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez.md
---
sldb:
  by: agent
  at: '2026-11-11T09:31:40Z'
  authority: generated
  via: create_document
id: task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez
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
- src/sldb/api/stores/
- tests/store/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-un-documento-que-cae-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-dos-veces.md
---

# Un documento en el glob de un modelo padre y en los paths de un modelo hijo se trackea una sola vez, bajo el hijo (gana el más específico)

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del coordinador, delante de H9. Rompe deskops view board en todo store de deskops construido en limpio (clon nuevo o CI): cada tarea queda trackeada dos veces y los selectores por nombre dan Ambiguous task selector.

## Goal

_Describe the concrete result this task must produce._

sldb resuelve un path nombrado por varias reglas include a una sola fila: gana el modelo hijo por paths sobre el glob del padre; sin herencia, error store/include-conflict; un store ya duplicado se corrige en el próximo build.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/, tests/store/, tests/api/, docs/, CHANGELOG.md. Fuera: store.yaml de deskops y una vía de CLI para quitar includes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del coordinador (2026-11-11, revisable): prioridad POR DELANTE de H9, detrás de la tarea de seguridad live_stale. Nota de origen: inbox 6f9576a7 (glob de modelo padre y paths de modelo hijo). Deskops la espera en su drawer bcf090a8.

REPRODUCCIÓN (coordinador; log runs/subagents/20261111-repro-dbltrack/repro.log): checkout limpio de deskops origin/main 64a5bcc7 con sldb 9c9dac6b. .sldb/store.yaml declara 'model: TaskDoc, glob: desk/tasks/task-*.md' y además cada tarea por 'paths' en su modelo hijo (TaskCodeDoc, TaskDebugDoc). Tras 'rm -rf .sldb_cache && sldb stores build --store .sldb' (rc 0), cada una de las 3 tareas queda trackeada dos veces (TaskDoc y su hijo). 'deskops view board' da 0 tareas y un 'Ambiguous task selector' por tarea. Lo hace cualquier clon nuevo y el CI; con una caché vieja no se ve.

CAUSA: src/sldb/api/stores/declared_files.py declared_files suma las filas (model, path, name) de cada regla include sin mirar si un mismo path ya lo nombra otra regla. apply_includes trackea cada fila, así que un archivo que cae en el glob del padre y en los paths del hijo queda trackeado bajo los dos modelos.

ARREGLO (vía fijada por el coordinador: gana el modelo más específico; no se toca store.yaml):
t1 (resolución): cuando un mismo path lo nombran varias reglas include, gana una sola fila. La de 'paths' explícitos gana sobre la de 'glob' si su modelo es descendiente del modelo del glob (herencia de modelos del store: base_names / contrato). Entre dos reglas del mismo tipo, o con modelos sin relación de herencia, no se elige: build y stores check dan un error 'store/include-conflict' que nombra el path y los modelos.
t2 (stores declare --write): conserva el glob autorado como hoy; con t1 ya no duplica.
t3 (un store ya construido con duplicados): el próximo build o stores update destrackea la fila perdedora (la del glob padre) y deja la del hijo, sin tocar el archivo. Idempotente.
t4 (tests): un store de prueba con modelo padre por glob y modelo hijo por paths sobre los mismos archivos, construido en limpio (sin caché). Cada archivo queda trackeado una sola vez bajo el hijo. Un selector por nombre resuelve sin ambigüedad. t3 se prueba sobre un store ya duplicado. El conflicto entre modelos sin herencia da el error. El test va en tests/store/ para que el CI construya en limpio.
t5 (deskops): el informe dice si el drawer de deskops bcf090a8 (quitar o migrar el glob TaskDoc) sigue haciendo falta con t1.

VALIDACIÓN: el worker corre los tests que toca, tests/store y tests/api de stores (build, declare, update, check), test_clean_code_rules y tools/check.sh --fast. Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml; api/stores ya es carpeta declarada. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test en tests/store con padre por glob e hijo por paths, build en limpio: una sola fila bajo el hijo
- Selector por nombre sin ambigüedad; store ya duplicado corregido por build/update (idempotente)
- Conflicto sin herencia da store/include-conflict
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

t1-t5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.

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
Cold-bundle de la tarea task-un-documento-en-el-glob-de-un-modelo-padre-y-en-los-paths-de-un-modelo-hijo-se-trackea-una-sola-vez: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test en tests/store con padre por glob e hijo por paths, build en limpio: una sola fila bajo el hijo
- Selector por nombre sin ambigüedad; store ya duplicado corregido por build/update (idempotente)
- Conflicto sin herencia da store/include-conflict
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio


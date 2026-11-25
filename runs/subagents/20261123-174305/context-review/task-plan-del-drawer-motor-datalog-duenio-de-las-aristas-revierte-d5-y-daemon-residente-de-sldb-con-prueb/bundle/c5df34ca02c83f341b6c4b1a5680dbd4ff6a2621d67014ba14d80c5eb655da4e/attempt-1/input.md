FILE:desk/tasks/task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb.md
---
sldb:
  by: agent
  at: '2026-11-23T17:38:45Z'
  authority: generated
  via: save_document_payload
id: task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-142527-suggestion-decisi-n-de-jp-el-grafo-de-sldb-pasa-a-un-motor-datalog-revierte-d5.md
- desk/inbox/20261123-142553-suggestion-jp-pide-ver-ahora-el-daemon-de-sldb.md
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Plan del drawer: motor Datalog duenio de las aristas (revierte D5) y daemon residente de sldb, con prueba de concepto medida y decisiones para JP

## Rationale

_Explain why this task exists or the business driver behind it._

Notas 20261123-142527-suggestion-decisi-n-de-jp-el-grafo-de-sldb-pasa-a-un-motor-datalog-revierte-d5 y 20261123-142553-suggestion-jp-pide-ver-ahora-el-daemon-de-sldb (JP 2026-11-23): JP revierte D5 de desk/drawer/plans/grafo-operable/decisiones.md y pide que el grafo pase a un motor Datalog estable que sea duenio del almacenamiento y la consulta de aristas (hoy GraphBackend en src/sldb/store/graph/backend/protocol.py solo cubre eval/analyze sobre networkx; componer el indice, federar stores y live stale van a mano sobre YAML en .sldb_cache/edges: 28 s la primera carga del indice federado, specir catalog build no termina en 280 s). Tambien pide ver ahora el daemon de sldb (diferido desde 2026-11-15): un proceso residente con el indice de aristas y el store cargados para que el CLI, sldb serve, deskops y specir no recompongan el indice en cada invocacion.

## Goal

_Describe the concrete result this task must produce._

Existe desk/drawer/plans/grafo-datalog-daemon/ con alcance, brief, decisiones y dag.yaml que cubre las dos cosas juntas; decisiones.md de grafo-operable registra D5 revertida por JP el 2026-11-23; el plan trae los resultados de una prueba de concepto que carga el indice federado real en un motor Datalog embebido (Datalevin u otro con cliente Python) y mide aristas de un nodo, recorrido, emparejamiento de atomos y stale contra el camino actual; y cada decision de diseno abierta queda como una task.decision para JP.

## Scope

_State what is in scope and what is out of scope._

Entra: comparar motores Datalog con cliente Python (Datalevin como candidato de docs/architecture/graph-backend.md) y elegir uno para la prueba; prueba de concepto fuera del codigo de produccion (scripts en reports/ o en el plan) con mediciones; para el daemon: que queda residente, como lo encuentra el CLI, que pasa sin daemon en contenedores de ejecutor y en tests, como se invalida con git, relacion con sldb serve y con los hooks actuales, consumo de memoria en robocop2 con el tope de 8 GB libres; task.decision por cada decision (motor, forma del daemon, invalidacion). Fuera: cambiar GraphBackend o el codigo de produccion; eso sale de tareas que el plan propone. No reemplaza ni bloquea task-matching-attach-atom-edges-deja-de-recomponer-live-stale..., que va primero.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/graph-backend.md, desk/drawer/plans/grafo-operable/ y el codigo de GraphBackend, compose y edge_index. 2) Prueba de concepto: exportar el indice federado real a hechos y cargarlo en el motor; medir las cuatro consultas contra el camino actual, con RSS. 3) Escribir el plan (alcance, brief, decisiones, dag.yaml) con el daemon. 4) Registrar D5 revertida en grafo-operable/decisiones.md. 5) Crear las task.decision con deskops add task --task-type task.decision.

## Validation

_List the checks required before this task can close._

- deskops graph missing --root . sin faltantes nuevos; la prueba de concepto se puede repetir con el comando que deja el informe

## Done When

_Name the observable condition that makes the task complete._

El plan existe con dag.yaml valido (deskops review node puede leerlo); el informe trae la tabla de tiempos y memoria de la prueba de concepto contra el camino actual; D5 aparece como revertida con fecha y motivo; hay una task.decision por decision abierta, con opciones y recomendacion.

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
Cold-bundle de la tarea task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- deskops graph missing --root . sin faltantes nuevos; la prueba de concepto se puede repetir con el comando que deja el informe


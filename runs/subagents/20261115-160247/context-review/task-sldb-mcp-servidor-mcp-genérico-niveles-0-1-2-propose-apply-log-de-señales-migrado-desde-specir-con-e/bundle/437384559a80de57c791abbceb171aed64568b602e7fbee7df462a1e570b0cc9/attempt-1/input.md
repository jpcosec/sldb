FILE:desk/tasks/task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e.md
---
sldb:
  by: agent
  at: '2026-11-15T15:50:32Z'
  authority: generated
  via: create_document
id: task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e
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

# sldb mcp: servidor MCP genérico (niveles 0/1/2, propose/apply, log de señales) migrado desde specIR, con extra opcional mcp

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: nunca reimplementar en un consumidor lo que es de sldb. El servidor MCP de specIR no tiene nada de dominio: lee y escribe un store solo por sldb.api. Debe vivir en sldb y specIR montar encima sus tools de dominio.

## Goal

_Describe the concrete result this task must produce._

Comando 'sldb mcp --store <dir> --level 0|1|2 --actor <quien>' servido por stdio, instalable como extra opcional 'mcp' del paquete sldb, con las tools de lectura y de escritura de specIR migradas (no reescritas), el log de señales y un punto de extensión para tools de consumidores.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Origen: el paquete mcp de specIR (repo IR, main 82c79d6 para escritura IR04 y 14f6f24 para lectura IR03; módulos server, read_tools, write_tools, changes, mutability, addresses, paging) y sus tests (test_read_tools, test_no_writes, test_dry_run, test_mutability, test_write_tools, writing, más las fixtures de conftest que usan). Leerlos antes de escribir nada. Tools de lectura (nivel 0, todas read-only e idempotentes): list_models, describe_model, list_relation_types, describe_relation_type, read_document, select_documents, neighbors, neighborhood, list_views, resolve_view, check_integrity; JSON estructurado, dirección estable sldb://document/<export_id>, conjuntos paginados {items,total,offset,limit,truncated,next_offset}. Tools de escritura (nivel 1 contenido, nivel 2 reglas como dato; el nivel lo fija el operador al arrancar, nunca un argumento de tool; los modelos como código nunca se sirven): propose_changes (ejecución en seco con las guardas expected_source_hash puestas por el servidor, no escribe) y apply_changes (la propuesta tal cual; todo o nada, rechazo con causa stale o rules) sobre sldb.api.apply_batch; --actor firma la procedencia. Adaptación: quitar de lo migrado todo lo específico de specIR (nombres, tests que dependen de la federación spec2viz o de tareas concretas del board de IR: reescribir la fuente de verdad de esos tests contra el propio store de sldb, sin literales que repitan la respuesta). Extra opcional 'mcp' en pyproject (dependencia mcp>=2.2), importación perezosa para que sldb sin el extra siga funcionando y 'sldb mcp' diga cómo instalarlo; subcomando registrado en la CLI respetando contracts/layers.toml. LOG DE SEÑALES (decisión de JP, punto 3): cada consulta que pide algo que no existe o que se llama distinto se registra, y no es un error: tool desconocida, modelo, documento, campo, tipo de relación o vista inexistente, argumento no reconocido. La respuesta dice 'no implementado / no existe, registrado como señal' y sugiere nombres cercanos con sldb.api.matching (no un matcher nuevo). Cada entrada lleva momento, tool, argumentos, clase de señal, sugerencias y actor si lo hay. Se lee con una tool del MCP (por ejemplo list_signals, paginada como las demás). Funciona también en nivel 0: el log no es una escritura del store ni de los almacenados, así que no rompe la prueba de que leer no escribe. El worker decide dónde vive (runtime o caché del store, fuera de los documentos trackeados) y lo justifica en el informe de cierre. PUNTO DE EXTENSIÓN: una función pública (por ejemplo build_server con un registro de extensiones) para que un consumidor, specIR, registre tools de dominio encima del servidor de sldb sin copiarlo, heredando niveles, actor, paginación y log de señales; con un test que registra una tool de ejemplo. DESHACER: conecta con el pedido de sldb en el inbox 20261115-123855 (apply_batch devuelve el lote inverso con guardas, deshacer es de sldb por decisión de JP). Esta tarea no implementa el inverso en sldb.api; cuando ese pedido se resuelva, el MCP expone una tool undo_changes que reaplica el inverso; dejar el punto preparado y declarado como pendiente. Tests portados: cliente MCP real por stdio contra el servidor real, sobre copia aislada del store, comprobación de que leer no escribe (digest del store y de los enlazados antes y después), niveles, rechazo stale, reglas, aristas contra su tipo de relación. Sin mocks. Documentar en docs y CHANGELOG.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el origen en IR y listar qué importa de specir (debería ser solo sldb.api y mcp). 2) Copiar los módulos al paquete sldb con el mínimo cambio y portar los tests. 3) Registrar 'sldb mcp' en la CLI y el extra mcp. 4) Añadir el log de señales y list_signals con sugerencias de sldb.api.matching. 5) Añadir el punto de extensión con su test. 6) Documentar el pedido de deshacer como pendiente conectado al inbox 20261115-123855. 7) Suite completa de a un archivo, tools/check.sh y stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de cada archivo de tests tocado y después de cada tests/*.py de a uno
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin referencias nuevas

## Done When

_Name the observable condition that makes the task complete._

Existe 'sldb mcp --store --level --actor' que sirve por stdio las once tools de lectura, propose_changes y apply_changes según el nivel, y list_signals; el código viene migrado del servidor de specIR y no reescrito; los tests portados pasan con cliente MCP real; leer (incluido registrar señales) no escribe en el store; el punto de extensión lo prueba una tool de ejemplo; el informe justifica dónde vive el log de señales. La suite de sldb completa pasa (pytest de a un archivo con TMPDIR=/dev/shm, tools/check.sh, sldb stores build --check).

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
Cold-bundle de la tarea task-sldb-mcp-servidor-mcp-genérico-niveles-0-1-2-propose-apply-log-de-señales-migrado-desde-specir-con-e: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q de cada archivo de tests tocado y después de cada tests/*.py de a uno
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin referencias nuevas


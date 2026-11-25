FILE:desk/tasks/task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi.md
---
sldb:
  by: agent
  at: '2026-11-16T04:10:38Z'
  authority: generated
  via: create_document
id: task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md
depends_on: []
pills: []
files:
- src/sldb/api/views/view_source.py
- src/sldb/api/views/view_revision.py
- tests/api/test_run_view_reads.py
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# run_view dice que el store no está construido en vez de Unknown view (H12) y se reproduce si la revision depende de cachés del proceso (H13)

## Rationale

_Explain why this task exists or the business driver behind it._

CC34 de deskops dejó dos huecos de sldb.api.run_view: (H12) con .sldb_cache borrado, run_view responde "Unknown view: board" porque el índice sale vacío ("reading never rebuilds"), en vez de decir que hay que correr sldb stores build; el error sale de src/sldb/api/views/view_source.py:33. (H13) en el proceso que escribió el store, run_view da otra revision (src/sldb/api/views/view_revision.py:16, sha256 de source_hash, content_hash y shards_signature) para las mismas filas que un proceso nuevo o sldb serve; no está reproducido en sldb. H9 y H11 ya se resolvieron (04a0e94e, 47b75674) y H1-H8 van en una task.decision aparte. Origen: desk/inbox/inbox-note-viewdoc-run-view-lo-que-el-modelo-no-expresa-para-las-vistas-de-deskops-h1-h8-y-huecos-de-run-view-h.md.

## Goal

_Describe the concrete result this task must produce._

(H12) run_view sobre un store cuyo índice compuesto está vacío o sin construir lanza SLDBStoreError con "store index not built: run `sldb stores build`" en lugar de "Unknown view"; (H13) un test dice si la revision cambia entre el proceso que escribió y uno nuevo, y si cambia, la revision deja de depender de cachés en memoria.

## Scope

_State what is in scope and what is out of scope._

Entra: (H12) en view_source.py, antes de "Unknown view", distinguir índice vacío o sin shards (usar la misma señal que stores check usa para store/unbuilt, src/sldb/api/stores/store_surroundings.py) y lanzar el error de Goal; test en tests/api/test_run_view_reads.py que borra .sldb_cache y comprueba el mensaje. (H13) test en tests/api/test_run_view_reads.py que escribe un documento, corre run_view en el mismo proceso y en un subprocess nuevo (python -c con sldb.api.run_view) sobre el mismo store y compara revision; si difieren, encontrar qué entrada de view_revision.revision viene de una caché del proceso (source_hash del índice, content_hash o shards_signature) y leerla del disco; si no difieren, el test queda como guarda y el informe lo dice. CHANGELOG.md. No entra: H1-H8 (task.decision aparte), rendimiento de run_view (task-sldb-views-run-board-en-menos-de-1-s...).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer view_source.py, view_revision.py, store_surroundings.py y tests/api/test_run_view_reads.py. 2) Test H12 y arreglo. 3) Test H13 con subprocess; arreglo solo si falla. 4) Informe con el resultado de H13.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los dos tests nuevos; el informe dice si H13 se reprodujo; CHANGELOG y commit; aviso a deskops con deskops message send --to deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-run-view-dice-que-el-store-no-está-construido-en-vez-de-unknown-view-h12-y-se-reproduce-si-la-revisi: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


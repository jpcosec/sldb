FILE:desk/tasks/task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do.md
---
sldb:
  by: agent
  at: '2026-11-17T02:09:28Z'
  authority: generated
  via: create_document
id: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-222911-unclear-docs-list-incluye-un-documento-que-docs-show-no-encuentra-unknown-document-target.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/docs.py
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs list y docs show leen la misma fuente: no se lista un documento que show no encuentra (Unknown document target)

## Rationale

_Explain why this task exists or the business driver behind it._

En el store de sldb-ui, docs list --format json devuelve edge-task-v8-...-to-activate, pero docs show de ese nombre da 'Unknown document target' (500 en la API de sldb-ui); el nombre no está en .sldb/core/store_index.yaml. Origen: desk/inbox/20261116-222911-unclear-docs-list-incluye-un-documento-que-docs-show-no-encuentra-unknown-document-target.md.

## Goal

_Describe the concrete result this task must produce._

docs list y docs show coinciden: todo nombre que lista docs list se puede mostrar con docs show, o docs list lo marca como no resoluble con su causa.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar de qué fuente lee cada uno (src/sldb/cli/commands/docs.py y la API que llaman), reproducir con un store de prueba con un documento declarado o derivado que no está en el índice, y alinear las dos lecturas; test en tests/test_cli_v2.py. CHANGELOG. No entra: cambiar el formato de salida de docs list salvo el marcado de no resoluble.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs.py y las funciones de listado y de resolución. 2) Reproducir en tmp_path. 3) Alinear. 4) Test. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_select_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; result-summary.md explica de dónde salía el nombre fantasma; CHANGELOG y commit; aviso a sldb-ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


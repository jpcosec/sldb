Task: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do
Title: docs list y docs show leen la misma fuente: no se lista un documento que show no encuentra (Unknown document target)
Status: active
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-19T06:13:33Z'
  authority: generated
  via: save_document_payload
id: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-32f0e140e7fc FALLA sobre 9fbb1b77 (informe
  en runs/subagents/exec-deskops-t-32f0e140e7fc-testing/result-summary.md). El fix
  solo marca archivos ausentes o ilegibles. En el store real de UIs/sldb-ui el nombre
  edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate sigue
  listado sin marca: su .md y su YAML del índice existen, pero el modelo deskops.models:EdgeDoc
  no se puede importar (SLDBModelError: Attribute ''EdgeDoc'' not found in ''deskops.models''),
  así que load_runtime_documents no lo carga y docs show da Unknown document target.
  Intento 2: marcar también la causa model-not-importable (resolviendo el model_ref
  con el mismo pythonpath que usa docs show), con un test sobre un store de prueba
  cuyo model_ref no se importa, y verificar contra /mnt/ssd/proyectos/SLDB_1/UIs/sldb-ui
  si existe.'
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

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

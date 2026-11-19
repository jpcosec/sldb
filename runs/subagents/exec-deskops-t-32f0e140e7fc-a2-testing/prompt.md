Task: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do
Title: docs list y docs show leen la misma fuente: no se lista un documento que show no encuentra (Unknown document target)
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T06:18:12Z'
  authority: generated
  via: save_document_payload
id: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
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
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-docs-list-y-docs-show-leen-la-misma-fuente-no-se-lista-un-documento-que-show-no-encuentra-unknown-do"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.

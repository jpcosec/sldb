FILE:desk/tasks/task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared.md
---
sldb:
  by: agent
  at: '2026-11-17T06:36:56Z'
  authority: generated
  via: create_document
id: task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021515-suggestion-read-store-dice-store-not-prepared-para-un-store-inexistente.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/read_store.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# read_store distingue un store inexistente ('store not found') de uno sin preparar ('store not prepared')

## Rationale

_Explain why this task exists or the business driver behind it._

sldb.api.read_store (src/sldb/api/stores/read_store.py) lanza 'store not prepared: run sldb stores update' también cuando el store no existe, porque store_is_prepared devuelve False si falta .sldb o core/store_index.yaml; correr stores update no sirve en ese caso y graph_ui responde 503 guiando mal al operador. Origen: desk/inbox/20261117-021515-suggestion-read-store-dice-store-not-prepared-para-un-store-inexistente.md.

## Goal

_Describe the concrete result this task must produce._

read_store lanza SLDBStoreError 'store not found: <ruta>' cuando no existe el directorio del store, y conserva 'store not prepared: run sldb stores update (<ruta>)' cuando el store existe pero le falta el índice.

## Scope

_State what is in scope and what is out of scope._

Entra: distinguir los dos casos en read_store.py (y en store_is_prepared si hace falta), con el mismo tipo de excepción; tests en tests/api/test_api_stores.py para los dos mensajes. CHANGELOG. No entra: cambiar otros mensajes.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer read_store.py y _resolve_store_arg. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a graph_ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


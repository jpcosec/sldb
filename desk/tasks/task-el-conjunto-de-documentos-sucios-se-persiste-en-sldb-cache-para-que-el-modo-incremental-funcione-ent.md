---
sldb:
  by: agent
  at: '2026-11-17T02:48:38Z'
  authority: generated
  via: create_document
id: task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/documents_dirty.py
- tests/store/test_merkle_operation_cache.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El conjunto de documentos sucios se persiste en .sldb_cache para que el modo incremental funcione entre corridas (V2)

## Rationale

_Explain why this task exists or the business driver behind it._

Para la mejora de velocidad V2, el conjunto de documentos sucios (src/sldb/store/documents_dirty.py) vive solo en la memoria del proceso: cada corrida nueva no sabe qué cambió y el modo incremental no sirve entre procesos. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

El conjunto de documentos sucios se guarda en .sldb_cache (regenerable, sin versionar) y una corrida nueva lo lee, de modo que una actualización incremental en un proceso nuevo procesa solo lo que cambió; si el archivo falta o está corrupto, se vuelve al cálculo completo sin error.

## Scope

_State what is in scope and what is out of scope._

Entra: persistir y leer el conjunto en .sldb_cache con escritura atómica y bajo el lock del store; invalidarlo cuando cambia la firma del store; tests en tests/store/test_merkle_operation_cache.py o un archivo de tests de store existente (proceso nuevo ve el dirty del anterior; archivo corrupto cae al cálculo completo). CHANGELOG. No entra: versionar el archivo, cambiar qué se considera sucio.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer documents_dirty.py, user_cache.py y quién consume el conjunto. 2) Implementar persistencia y lectura. 3) Tests con subprocess. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_operation_cache.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_runtime_wiped.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_edges_follow_the_contract.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit.

---
sldb:
  by: agent
  at: '2026-11-21T12:14:37Z'
  authority: generated
  via: save_document_payload
id: task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- contracts/layers.toml
- src/sldb/store/documents_dirty.py
- src/sldb/store/documents_dirty_persist.py
- tests/store/test_merkle_operation_cache.py
- 6772820a48ee1f43a57a32bc9a45c3509400af38
depends_on: []
pills: []
files:
- CHANGELOG.md
- contracts/layers.toml
- src/sldb/store/documents_dirty.py
- src/sldb/store/documents_dirty_persist.py
- tests/store/test_merkle_operation_cache.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb
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

Precisiones (coordinador, bundle-1): el archivo es documents_dirty.json en el directorio .sldb_cache del store que ya usa src/sldb/store/user_cache.py; JSON {"signature": <firma>, "entries": [[modelo, namespace, [nombres...]], ...]}. La firma es la de runtime_cache_signature.signature(s_path) (src/sldb/store/runtime_cache_signature.py) serializada. Escritura atómica (tmp + os.replace) dentro de store_lock (src/sldb/store/io/__init__.py). Carga perezosa: la primera llamada a names() para un store lee el archivo una vez y llena _DIRTY; mark, clear e invalidate reescriben el archivo. Corrupto = no parsea como JSON o no tiene esas claves: se borra el archivo y names() devuelve None (cálculo completo), sin log ni error. La lógica nueva va a un módulo nuevo documents_dirty_persist.py en el paquete sldb.store para que documents_dirty.py no pase de 80 líneas.

Precisiones (coordinador, bundle-2): los tests nuevos van en tests/store/test_merkle_operation_cache.py. La firma se guarda como json.dumps(list(signature), default=str) y se compara por igualdad de esa cadena. Cada mark, clear o invalidate toma store_lock y reescribe el archivo entero. Corrupto también incluye entries con forma distinta de [str, str, [str...]]. El límite de 80 líneas es el que mide tests/test_clean_code_rules.py.

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

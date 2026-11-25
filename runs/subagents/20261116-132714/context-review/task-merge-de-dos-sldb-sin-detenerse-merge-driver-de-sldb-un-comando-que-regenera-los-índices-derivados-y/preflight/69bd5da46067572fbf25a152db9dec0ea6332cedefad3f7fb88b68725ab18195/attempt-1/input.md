FILE:desk/tasks/task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y.md
---
sldb:
  by: agent
  at: '2026-11-16T13:12:18Z'
  authority: generated
  via: create_document
id: task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md
depends_on: []
pills: []
files:
- src/sldb/store/io/__init__.py
- src/sldb/api/stores/update_store_indexes.py
- src/sldb/cli/parsers/stores.py
- tests/store/test_update_fault_tolerance.py
- tests/store/test_merkle_shards.py
- docs/versionado-y-colaboracion.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Merge de dos .sldb sin detenerse: merge driver de sldb, un comando que regenera los índices derivados y un error que dice exactamente qué correr (une la decisión de JP y H2 de velocidad-hooks)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP (2026-11-16, vía supervisor) sobre la tarea task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam: hacerlo mucho más explícito, para que los agentes dejen de detenerse al mezclar dos .sldb. Hoy cualquier escritura reescribe .sldb/core/store_index.yaml (store_hash) y .sldb/core/models/<Modelo>.yaml (roster_hash, documents_count), así que dos ramas que tocan documentos distintos siempre chocan ahí aunque los shards se mezclen limpios; sldb stores update empieza con load_store_index (src/sldb/store/io/__init__.py:79), que falla con los marcadores de conflicto, y no hay .gitattributes ni merge driver (en a3514755 se quitaron a mano). Une con H2 de velocidad-hooks-brief.md (merge driver para los índices generados que regenera en vez de marcar conflicto, une los include de store.yaml, aviso en stores init si otra rama ya tiene store, procedimiento documentado) y responde la nota de MEPU 20261115-195033 (un store por rama). Origen: desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md.

## Goal

_Describe the concrete result this task must produce._

Un merge o rebase de dos ramas que tocaron .sldb termina sin intervención: el merge driver de sldb resuelve store_index.yaml y models/*.yaml y une los include de store.yaml; si aun así quedan índices derivados ilegibles (por ejemplo, marcadores de un merge hecho sin el driver), cualquier comando de sldb que los lea falla con un mensaje que dice el comando exacto a correr, y ese comando los regenera desde los shards. El procedimiento está en AGENTS.md del repo y en la ayuda del CLI.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) `sldb stores rebuild-index`: regenera .sldb/core/store_index.yaml y .sldb/core/models/*.yaml desde los shards de .sldb/core/documents/ y el contrato de cada modelo, sin leer los índices derivados actuales (los ignora si tienen marcadores o no parsean); usa las funciones que ya calculan esos niveles (documents_hash._hash_b, hashing.hash_model_layer, ops.cascade_store_hash; localizarlas con grep). (2) `sldb stores merge-driver %O %A %B %P`: para un archivo derivado (store_index.yaml o models/*.yaml) deja en %A la versión de la rama actual y sale 0 (el índice correcto lo deja rebuild-index); para .sldb/store.yaml une las listas include de las dos ramas (por model, sin duplicar rutas) y conserva lo demás de %A; para cualquier otro archivo sale 1 (conflicto normal). (3) `sldb stores merge-driver --install`: escribe en .gitattributes del repo las líneas `.sldb/core/store_index.yaml merge=sldb`, `.sldb/core/models/*.yaml merge=sldb` y `.sldb/store.yaml merge=sldb`, y configura en .git/config `merge.sldb.driver = sldb stores merge-driver %O %A %B %P` y `merge.sldb.name`; es idempotente. (4) Mensaje de error: donde se carga store_index.yaml o un models/*.yaml (load_store_index y load_models_index en src/sldb/store/io/__init__.py) un archivo con marcadores `<<<<<<<` o que no parsea lanza SLDBStoreError con el texto exacto "<ruta> is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)". (5) `sldb stores init` avisa con una alerta si `git ls-tree` de otra rama local del mismo repo ya tiene .sldb/store.yaml. (6) Documentación: AGENTS.md nuevo en la raíz del repo de sldb con la sección "Merge de .sldb" (los tres comandos y cuándo), la misma sección en docs/versionado-y-colaboracion.md, y el help de los tres subcomandos. (7) Tests en tests/store/test_update_fault_tolerance.py y tests/store/test_merkle_shards.py: rebuild-index sobre un store con store_index.yaml y un models/*.yaml con marcadores deja índices iguales a los de un build limpio; el driver une includes de store.yaml; --install es idempotente; el mensaje de error es exacto. CHANGELOG.md. (8) Al cerrar: responder la nota de MEPU con deskops message send --to mepu explicando el procedimiento. No entra: H1 (hooks install), H3, H4; cambiar qué se versiona (lo hace la tarea de separar .sldb_store y .sldb_cache, que depende de esta); stores build completo como reemplazo de rebuild-index.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/io/__init__.py (load_store_index, load_models_index), src/sldb/api/stores/update_store_indexes.py, src/sldb/cli/parsers/stores.py y el comando de stores en src/sldb/cli/commands/, y las funciones de hash citadas. 2) Implementar rebuild-index en la API (src/sldb/api/stores/) y su subcomando. 3) Implementar merge-driver e --install. 4) Mensaje de error en la carga. 5) Aviso en stores init. 6) AGENTS.md, doc y help. 7) Tests y CHANGELOG. 8) Probar a mano en /dev/shm: dos ramas de un repo de prueba que tocan documentos distintos, merge con el driver instalado, sin conflicto; y merge sin driver, error exacto, rebuild-index, stores check verde.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos de Validation pasan con los tests nuevos; la prueba a mano de dos ramas (con y sin driver) queda en result-summary.md con su salida; AGENTS.md y docs/versionado-y-colaboracion.md tienen la sección "Merge de .sldb"; `sldb stores --help` lista rebuild-index y merge-driver; CHANGELOG y commit; nota respondida a mepu.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


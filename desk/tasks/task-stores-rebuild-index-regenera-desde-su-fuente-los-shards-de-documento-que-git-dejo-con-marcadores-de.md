---
sldb:
  by: agent
  at: '2026-11-23T01:35:55Z'
  authority: generated
  via: save_document_payload
id: task-stores-rebuild-index-regenera-desde-su-fuente-los-shards-de-documento-que-git-dejo-con-marcadores-de
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-205449-suggestion-ning-n-comando-de-sldb-repara-un-shard-de-documento-sldb-que-git-dej-en-conflicto.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# stores rebuild-index regenera desde su fuente los shards de documento que git dejó con marcadores de conflicto y quita los de documentos cuyo fuente ya no existe

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261120-205449 (IR, 2026-11-20): al fusionar una rama que tocaba desk/tasks/Board.md, git dejó en conflicto .sldb/core/documents/BoardDoc/Board.yaml (UU) y un shard DU. 'sldb stores rebuild-index' falla leyendo el shard con marcadores, y 'docs track --reindex' y 'docs update' también. Como .sldb no se toca a mano, el merge se abortó. En origin/main 6ab01b80 el driver cubre solo store_index.yaml, models/*.yaml y store.yaml (.gitattributes), y rebuild-index (src/sldb/api/stores/rebuild_index.py) solo repara con conflict_sides los índices derivados y store.yaml, no core/documents/**. La task.decision sobre conflictos en los índices derivados (task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam) no cubre los shards de documento.

## Goal

_Describe the concrete result this task must produce._

Con un shard de documento con marcadores de conflicto, 'sldb stores rebuild-index' lo regenera desde su archivo fuente, como lo haría docs track --reindex. Si el fuente ya no existe, quita el shard y su entrada del índice. El comando reporta los shards reparados y quitados, y después stores check sale sin errores.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/stores/rebuild_index.py (detectar shards con has_conflict_markers de src/sldb/store/io/derived_guard.py, o shards que no parsean, bajo core/documents/), la regeneración del shard reutilizando el camino de docs track --reindex, y tests en tests/store/ que dejan un shard con marcadores y otro huérfano y corren rebuild-index. CHANGELOG.md. Fuera: ampliar el merge driver a core/documents/**; si el ejecutor lo ve necesario, lo anota en el informe.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test con un store de prueba: shard con marcadores para un documento cuyo .md existe, y shard de un documento cuyo .md se borró. 2) rebuild-index repara el primero desde el .md y quita el segundo, y lo devuelve en su reporte ('repaired'/'removed'). 3) stores check limpio. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (shard regenerado igual al que da docs track --reindex; huérfano quitado); la suite completa sale rc 0.

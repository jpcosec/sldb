FILE:desk/tasks/task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update.md
---
sldb:
  by: agent
  at: '2026-11-16T05:27:44Z'
  authority: generated
  via: save_document_payload
id: task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-edgeindex-stale-go04-d7eefdeb-manda-a-reconstruir-pero-rebuild-edges-no-resuelve-una-edición-externa.md
depends_on: []
pills: []
files:
- src/sldb/store/edge_index/edge_index.py
- src/sldb/api/edges/edge_reading.py
- src/sldb/cli/commands/edges.py
- tests/api/test_api_edges.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# EdgeIndex.stale manda a la operación correcta: una edición externa se resuelve con sldb stores update, no con edges rebuild

## Rationale

_Explain why this task exists or the business driver behind it._

Desde GO04 (d7eefdeb) live_stale compara cada archivo trackeado con el source_hash de su shard: una edición externa deja el documento en EdgeIndex.stale. Pero los textos que acompañan a stale mandan a reconstruir: la descripción del campo (src/sldb/store/edge_index/edge_index.py:19, "run the rebuild"), la docstring de load_edge_index (src/sldb/api/edges/edge_reading.py:17-18, "rebuild_edges brings them current") y la alerta edges/stale de la CLI (src/sldb/cli/commands/edges.py:73, fix "sldb edges rebuild"). rebuild_edges compara con el hash registrado del store y da docs_written=0, así que stale queda para siempre y graph_ui bloquea el grafo. La docstring de rebuild_edges (src/sldb/api/edges/rebuild_edges.py:21-23) ya dice que la edición externa se resuelve con update_store_indexes. Origen: desk/inbox/inbox-note-edgeindex-stale-go04-d7eefdeb-manda-a-reconstruir-pero-rebuild-edges-no-resuelve-una-edición-externa.md.

## Goal

_Describe the concrete result this task must produce._

Los tres textos nombran `sldb stores update` (API update_store_indexes) como la operación que resuelve un documento stale por edición externa, y un test prueba que después de stores update el documento editado sale de stale.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar la descripción del campo stale en edge_index.py, la docstring de load_edge_index en edge_reading.py y la alerta de _report_findings en src/sldb/cli/commands/edges.py (what: "tracked file changed since its shard was built", fix: "sldb stores update"). Test nuevo en tests/api/test_api_edges.py: editar a mano un documento de un store de prueba -> aparece en load_edge_index(...).stale -> rebuild_edges no lo saca -> update_store_indexes sí. Si el test muestra que update_store_indexes tampoco lo saca, la tarea se detiene y el ejecutor reporta el caso (no se cambia rebuild_edges en esta tarea). CHANGELOG.md. No entra: que rebuild_edges rehashee archivos, ni stale por documento en graph_ui.

Precisiones (preflight-1): textos exactos. Descripción del campo stale: "Export ids of tracked documents whose shard is missing, built from another hash_c or EDGE_INDEX_VERSION, from a file since edited outside sldb, or under another contract_signature of the model: `sldb stores update` (update_store_indexes) brings them current; `sldb edges rebuild` only rebuilds shards from the hashes the store already recorded." Docstring de load_edge_index: reemplazar "`rebuild_edges` brings them current" por "`update_store_indexes` (`sldb stores update`) brings them current". Alerta: alert("edges/stale", s, "tracked file changed since its shard was built", "sldb stores update"). Del grep solo se cambian los mensajes cuyo texto habla de stale o de documentos editados fuera de sldb; los que hablan de reconstruir el índice por versión o por shards faltantes quedan. tests/api/test_composition_edges.py se corre como regresión y no se modifica. El store de prueba se arma como en los tests existentes de tests/api/test_api_edges.py.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer los cuatro archivos citados. 2) Escribir primero el test. 3) Cambiar los textos. 4) grep -rn "edges rebuild" src/sldb docs/ para encontrar otros mensajes que manden a reconstruir por stale y alinearlos.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_composition_edges.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (stale -> stores update -> no stale); los mensajes ya no dicen rebuild para stale; CHANGELOG y commit; aviso a graph_ui con deskops message send --to graph_ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


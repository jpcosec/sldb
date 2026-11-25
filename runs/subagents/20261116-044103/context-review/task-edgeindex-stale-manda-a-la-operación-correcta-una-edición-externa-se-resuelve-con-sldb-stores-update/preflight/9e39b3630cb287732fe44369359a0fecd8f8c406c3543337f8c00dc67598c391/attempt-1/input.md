FILE:desk/tasks/task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update.md
---
sldb:
  by: agent
  at: '2026-11-16T04:08:05Z'
  authority: generated
  via: create_document
id: task-edgeindex-stale-manda-a-la-operación-correcta-una-edición-externa-se-resuelve-con-sldb-stores-update
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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


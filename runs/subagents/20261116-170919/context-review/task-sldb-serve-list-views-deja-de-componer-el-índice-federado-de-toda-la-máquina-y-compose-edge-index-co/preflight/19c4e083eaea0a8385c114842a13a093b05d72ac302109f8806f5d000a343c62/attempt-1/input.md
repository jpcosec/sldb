FILE:desk/tasks/task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co.md
---
sldb:
  by: agent
  at: '2026-11-16T16:29:43Z'
  authority: generated
  via: create_document
id: task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-101851-suggestion-sldb-serve-list-views-compone-el-ndice-federado-de-toda-la-m-quina-en-fr-o-y-sin-lock-2-5-gb-por-proceso.md
depends_on: []
pills: []
files:
- src/sldb/api/views/list_views.py
- src/sldb/store/edge_index/compose.py
- tests/api/test_views_linked.py
- tests/store/test_shard_cache_copies.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta
---

# sldb serve: list_views deja de componer el índice federado de toda la máquina y compose_edge_index compone una sola vez por clave aunque lleguen peticiones concurrentes

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui midió en robocop2 (2026-11-16) que el sldb serve que levanta su test se va a 2-5 GB por proceso: seis hilos de petición estaban en list_views -> load_edge_index(include_linked=True) -> compose_edge_index -> read_or_compose -> ... -> load_edges_shard con model_copy(deep=True); componer una vez federa 7 stores, 15.617 shards, 178.756 aristas, 35,5 s y 1,2 GB. list_views (src/sldb/api/views/list_views.py:24) pide la federación entera solo para listar nodos ViewDoc; compose_edge_index (src/sldb/store/edge_index/compose.py) guarda en un dict de módulo _COMPOSED sin lock, así que dos llamadas en frío componen dos veces a la vez. Bloquea los tests de graph_ui. Origen: desk/inbox/20261116-101851-suggestion-sldb-serve-list-views-compone-el-ndice-federado-de-toda-la-m-quina-en-fr-o-y-sin-lock-2-5-gb-por-proceso.md (evidencia en UIs/graph_ui/runs/subagents/20261116-sldb-serve-rss/ del workspace SLDB_1).

## Goal

_Describe the concrete result this task must produce._

list_views devuelve las mismas vistas que hoy (locales y de stores enlazados, H9) sin llamar a compose_edge_index, y N llamadas concurrentes en frío a compose_edge_index con la misma clave componen una sola vez; el caso mínimo de graph_ui ya no pasa de 1 GB.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) Un módulo nuevo view_nodes.py en el paquete sldb.api.views con una función que, para cada (ruta, nombre) de federated_stores(store_path, True) (src/sldb/store/edge_index/federation.py), lee solo los shards de aristas del modelo ViewDoc con compose_edges_documents(ruta, "ViewDoc", copy=False) (src/sldb/store/io/shard_compose.py), califica los nodos con qualify(part, nombre) como hace la composición, estampa facets.source.store_path y se queda con los nodos de node_type "ViewDoc"; list_views (src/sldb/api/views/list_views.py) la usa en lugar de load_edge_index. Se mantiene la federación transitiva que hay hoy. (2) Un módulo nuevo compose_lock.py en el paquete sldb.store.edge_index con un single-flight por clave: un threading.Lock de módulo que guarda un dict clave -> Lock; compose_edge_index toma el lock de su clave en la rama de fallo de caché y vuelve a mirar _COMPOSED adentro antes de componer. (3) Tests: en tests/api/test_views_linked.py, list_views con compose_edge_index parcheado para lanzar sigue listando la vista local y la enlazada; en tests/store/test_shard_cache_copies.py, 8 hilos que llaman a la vez compose_edge_index en frío sobre la misma clave cuentan una sola composición (monkeypatch del compositor interno con un contador). CHANGELOG.md. Al cerrar, aviso a graph_ui con deskops message send --to graph_ui. No entra: leer sin copia en read_store_contributions para todas las lecturas del índice (cambio global de semántica de copias; otra tarea si hace falta), limitar hilos en sldb serve, timeouts del cliente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer list_views.py, view_reading.py (run_view ya empieza local y amplía con widen), compose.py, composed_reading.py, federation.py, shard_compose.py y src/sldb/store/io/shards.py (camino copy=False). 2) Escribir view_nodes.py y cambiar list_views. 3) Escribir compose_lock.py y usarlo en compose_edge_index. 4) Tests. 5) Medir el caso mínimo de graph_ui (comando en el README de su evidencia) con /usr/bin/time -v y anotar el RSS máximo en result-summary.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views_linked.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_shard_cache_copies.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_run_view_reads.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los dos tests nuevos; result-summary.md tiene el RSS máximo del caso mínimo de graph_ui antes y después (después < 1 GB); CHANGELOG y commit; aviso a graph_ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-serve-list-views-deja-de-componer-el-índice-federado-de-toda-la-máquina-y-compose-edge-index-co: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


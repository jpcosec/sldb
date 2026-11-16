# Executor deskops-e-0d2adfe5edff: list_views sin federar el índice y compose_edge_index con single-flight

## Cambios
- `src/sldb/api/views/view_nodes.py` (nuevo): `view_nodes(store_path)` recorre `federated_stores(store_path, True)` (federación transitiva, como hoy), lee solo los shards de aristas del modelo ViewDoc con `compose_edges_documents(ruta, "ViewDoc", copy=False)`, califica con `qualify(shard, nombre)`, se queda con los nodos de `node_type == "ViewDoc"` (el primer contribuyente de un id gana, como `_merge`) y los estampa con `facets.source = {"store_path": ...}` (`_stamped`, copia superficial; los shards cacheados no se tocan). Devuelve los nodos ordenados por id, como `nodes_of_type`.
- `src/sldb/api/views/list_views.py`: `list_views` usa `view_nodes(...)` en vez de `load_edge_index(..., include_linked=True).nodes_of_type(VIEW_MODEL)`; docstring del módulo al día. `load_view`, `listed_name` y `summary` no cambian.
- `src/sldb/store/edge_index/compose_lock.py` (nuevo): `compose_lock(key)`: `threading.Lock` de módulo (`_GUARD`) que guarda un dict clave -> Lock.
- `src/sldb/store/edge_index/compose.py`: `compose_edge_index` en la rama de fallo de caché llama a `_composed_once` (nueva), que toma `compose_lock(key)`, vuelve a mirar `_COMPOSED` adentro y solo compone (`read_or_compose`) si sigue faltando o la firma no coincide. La rama de acierto sigue sin lock.
- `tests/api/test_views_linked.py::test_list_views_never_composes_the_federated_index`: con `compose_edge_index` parcheado para lanzar (en `edge_reading` y en `compose`), `list_views` lista la vista enlazada `board` (de B) y la local `mine`.
- `tests/store/test_shard_cache_copies.py::test_concurrent_cold_compositions_of_one_key_compose_once`: 8 hilos tras una `Barrier` llaman a la vez a `compose_edge_index` en frío sobre la misma clave, con `compose._compose` parcheado por un contador (más un sleep de 0,2 s para abrir la ventana de la carrera); hay una sola composición. Comprobado que **falla sin el lock** (con `compose_lock` reemplazado por un Lock nuevo por llamada: 1 failed).
- `CHANGELOG.md`: entrada en 0.1.13.

## Done When
- Validation: los 7 comandos con rc=0, con los dos tests nuevos (salida completa en `validation.log`):
  - `pytest -q tests/api/test_views_linked.py` rc=0
  - `pytest -q tests/api/test_views.py` rc=0
  - `pytest -q tests/store/test_shard_cache_copies.py` rc=0
  - `pytest -q tests/api/test_run_view_reads.py` rc=0
  - `pytest -q tests/test_serve.py` rc=0
  - `pytest -q tests/test_clean_code_rules.py` rc=0
  - `bash tools/check.sh --fast` rc=0 (TODAS LAS PUERTAS PASAN)
  (todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`).
- RSS máximo del caso mínimo de graph_ui, `tests/test_mindmap_deskops.py::test_real_advance_stale_origin_and_types`, con `/usr/bin/time -v` bajo `systemd-run --user --scope -p MemoryMax=3G` (logs completos en `rss-before.log` y `rss-after.log`):
  - **antes** (sldb de HEAD e70f09a6, `git archive HEAD src` puesto primero en `PYTHONPATH`): **2.239.812 kB (2,24 GB)**, 1:21 de pared, el test **falla** con el mismo `DeskError: sldb serve no respondió ... 502` del informe de graph_ui.
  - **después** (árbol de trabajo con este cambio): **103.720 kB (~104 MB)**, 0:17,7, el test **pasa**. < 1 GB: cumple.
  - Desvío: el README de la evidencia usa el venv `/dev/shm/venv-ir13-r2` de robocop2; este host es `Server` y ese venv no existe. Armé uno equivalente y temporal (`/dev/shm/venv-exec-leak`: uv venv 3.13, editables de sldb, deskops, pron y `UIs/graph_ui[deskops]`, más pytest), con `--basetemp` en /dev/shm; luego lo borré. La federación de este host la hacen los mismos enlaces transitivos (deskops, sldb, spec2viz, pron, scion...).
- CHANGELOG: hecho. **Commit: no hecho**, el brief lo prohíbe al ejecutor (lo hace el cierre/integrador). **Aviso a graph_ui (`deskops message send --to graph_ui`): no hecho**, escribe en desk/inbox y el brief prohíbe editar `desk/`; queda para el cierre del coordinador. Texto sugerido: "sldb: list_views ya no compone el índice federado (lee solo los shards de ViewDoc) y compose_edge_index compone una vez por clave con peticiones concurrentes; test_real_advance_stale_origin_and_types pasa de 2,24 GB y 502 a 104 MB y pass."

## Archivos tocados (exactos)
- `src/sldb/api/views/list_views.py` (modificado)
- `src/sldb/api/views/view_nodes.py` (nuevo; autorizado por el Scope (1))
- `src/sldb/store/edge_index/compose.py` (modificado)
- `src/sldb/store/edge_index/compose_lock.py` (nuevo; autorizado por el Scope (2))
- `tests/api/test_views_linked.py` (modificado)
- `tests/store/test_shard_cache_copies.py` (modificado)
- `CHANGELOG.md` (modificado)
- Evidencia: `runs/subagents/20261116-exec-leak/{validation.log,result-summary.md,rss-before.log,rss-after.log}`

## Notas y dudas
- Pills: la tarea no tiene pills atados; no hubo choque.
- `view_nodes` estampa en `facets.source` solo `store_path` (lo único que leen `view_source.view_store` y `list_views`), no `generated_from` ni `hash_a` como `_source` de la composición: así no lee `store_index` de cada store enlazado. Los nodos de `view_nodes` no salen fuera de `list_views`.
- La corrida "antes" compone el índice federado, que puede marcar documentos stale en el set dirty (`.sldb_cache`, derivado y sin trackear) de los stores enlazados, como hacía cualquier `sldb serve`. No toqué nada trackeado fuera de los archivos listados.
- Delegado al integrador: suite completa y `sldb stores build --check` (no figuran en Validation; no los corrí).
- Cambios ajenos del árbol (`apply_batch.py`, `lock.py`, `uv.lock`, `.sldb/`, `desk/runtimes/`, etc.): no tocados ni stageados.

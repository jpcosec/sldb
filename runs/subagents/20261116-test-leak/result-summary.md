# Tester deskops-t-8fa6a308e8be: list_views sin federar el índice + single-flight en compose_edge_index

**Veredicto: PASA** (en lo que toca al cambio. El commit y el aviso a graph_ui quedan para el cierre: ver Done When).

Salida completa en `validation.log` (en esta carpeta). Todo corrió con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`, salvo donde se indica.

## Cambio revisado
Cinco archivos del contrato (`list_views.py`, `compose.py`, `test_views_linked.py`, `test_shard_cache_copies.py`, `CHANGELOG.md`) y dos módulos nuevos sin trackear, `src/sldb/api/views/view_nodes.py` y `src/sldb/store/edge_index/compose_lock.py`. Ambos los pide el Scope (1) y (2), y el coordinador confirmó que son parte de la tarea.
- `view_nodes` recorre `federated_stores(store, True)` y lee `compose_edges_documents(ruta, "ViewDoc", copy=False)`. Califica con `qualify`, filtra `node_type == "ViewDoc"` y deja ganar al primer contribuyente, como `_merge`. Estampa `facets.source.store_path` con `model_copy`, así que no muta los shards cacheados. Se ajusta al Scope (1).
- `compose_lock` es un `threading.Lock` de módulo que guarda un dict clave → Lock (`setdefault` bajo la guarda). `_composed_once` toma el lock de la clave, vuelve a mirar `_COMPOSED` y recién entonces compone. La rama de acierto queda sin lock. Se ajusta al Scope (2).
- Detalle que no cambia nada: `_composed_once` pasa `key[2]`, que es el mismo `frozenset(exclude_tags)` de antes.
- Límite conocido, no es falla: el dict `_LOCKS` crece con cada clave distinta y no se limpia. En `sldb serve` el número de claves es pequeño (store × include_linked × tags × model_type_of).

## Validation (cada comando, corrido por mí)
| Comando | Resultado |
|---|---|
| pytest -q tests/api/test_views_linked.py | PASA: 7 passed, rc=0 (incluye el test nuevo) |
| pytest -q tests/api/test_views.py | PASA: 17 passed, rc=0 |
| pytest -q tests/store/test_shard_cache_copies.py | PASA: 4 passed, rc=0 (incluye el test nuevo) |
| pytest -q tests/api/test_run_view_reads.py | PASA: 6 passed, rc=0 |
| pytest -q tests/test_serve.py | PASA: 61 passed, rc=0 |
| pytest -q tests/test_clean_code_rules.py (obligatorio) | PASA: 1170 passed, rc=0 |
| bash tools/check.sh --fast (obligatorio) | PASA: rc=0, "TODAS LAS PUERTAS PASAN" |

Suite completa y `sldb stores build --check`: no figuran en Validation; quedan **delegados al integrador** y no los corrí.

## Done When, punto por punto
- **Validation pasa con los dos tests nuevos**: PASA (tabla de arriba). Además verifiqué que los dos tests detectan el fallo:
  - Con `compose_lock` reemplazado por un Lock nuevo en cada llamada (plugin `/dev/shm/tester-leak/plug/nolock_plugin.py`), `test_concurrent_cold_compositions_of_one_key_compose_once` falla (`assert len(composed) == 1`, rc=1).
  - Con el `src` de HEAD (`git archive HEAD src` a `/dev/shm/tester-leak/head`), `test_list_views_never_composes_the_federated_index` falla con `AssertionError: list_views composed the edge index` (rc=1).
- **RSS antes/después en result-summary (después < 1 GB)**: PASA. Revisé `runs/subagents/20261116-exec-leak/rss-before.log` y `rss-after.log`; por indicación del coordinador no repetí la medición, y los logs son coherentes.
  - Antes: `Maximum resident set size: 2239812` kB (2,24 GB), 1:21, `1 failed`, Exit status 1.
  - Después: `103720` kB (~104 MB), 0:17,7, `1 passed`, Exit status 0.
  - Comando: `tests/test_mindmap_deskops.py::test_real_advance_stale_origin_and_types` de graph_ui.
  - Salvedad: el ejecutor usó un venv propio (`/dev/shm/venv-exec-leak`) porque el de robocop2 no existe en este host.
- **CHANGELOG**: PASA. Entrada en 0.1.13 que nombra la task, la nota del inbox, los dos módulos y los dos tests; pasa la puerta de afirmaciones de check.sh --fast.
- **Commit**: PENDIENTE, del cierre. El ejecutor y el tester no hacen commit; no lo cuento como falla del cambio.
- **Aviso a graph_ui** (`deskops message send --to graph_ui`): PENDIENTE, del cierre, porque escribe en `desk/`. El ejecutor dejó un texto sugerido en su informe.

## Caso no cubierto por el ejecutor (script `/dev/shm/tester-leak/edge_cases.py`, rc=0)
1. **Federación transitiva A→B→C con choque de nombres**: hay `board` en A, B y C, y `deep` solo en C.
   - `view_nodes(A)` es **idéntico** a `load_edge_index(A, include_linked=True).nodes_of_type("ViewDoc")` en id, node_type, export_id, store y `facets.source.store_path`.
   - `list_views(A)` = `[('B:board','Board B'), ('C:board','Board C'), ('board','Board A'), ('deep','Deep')]`: la vista transitiva aparece y los choques se califican.
2. **Single-flight por clave, no global**: tres claves distintas (A, B, C), con `_compose` retrasado 0,5 s, componen en paralelo en 0,55 s, no 1,5 s.
3. **Firma cambiada después de cachear**: crear un documento nuevo provoca exactamente una recomposición, y el índice incluye el nodo nuevo.

## Regresiones vecinas
Los módulos de `src/` cambiados son `sldb.api.views.list_views` y `sldb.store.edge_index.compose`. Los archivos de `tests/` que los importan (`grep -rl`), corridos uno por uno:
- PASA: test_project_graph (13), test_guard_views (2), test_graph_backend (9), test_live_stale_security (8), test_payload_projection (40), test_predicate_language (16). Más los de Validation: test_views, test_views_linked, test_run_view_reads, test_shard_cache_copies.
- `tests/mcp/test_no_writes.py` y `tests/mcp/test_read_tools.py`:
  - Con `uv run --frozen --extra code --extra dev` dan error por `ModuleNotFoundError: No module named 'anyio'`. Es el entorno: el extra `mcp` no está instalado.
  - `--extra mcp` lo rechaza `uv run --frozen` porque el extra no figura en el `uv.lock`, que es ajeno.
  - Por eso los corrí con el respaldo del brief: `uvx --from "pytest>=8" --with-editable '.[mcp,code,dev]'`. Resultado: 2 passed y 14 passed.
- No hay fallas nuevas.

## Fuera del contrato
`git status --short`: fuera de los archivos del contrato y los dos módulos nuevos solo cambian:
- `.sldb/store.yaml`, `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml` y los dos `RunDoc/run-deskops-{e,t}-*.yaml`. Es el registro de las corridas que hace el despacho de deskops (agregan `runs/subagents/20261116-{exec,test}-leak/run.md`), no el ejecutor.
- `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/*`: ajenos.

El ejecutor no tocó nada más. Yo no edité el repo; mis scripts están en `/dev/shm/tester-leak/`.

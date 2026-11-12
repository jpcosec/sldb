# H11 worker report: run_view and the edge index per process

## Causa raíz (medida antes del cambio)
`run_view` armaba su estado con `load_edge_index(store, include_linked=True)` sin mirar qué podían
seleccionar las secciones, y el índice compuesto vivía solo en la memoria del proceso. Un proceso nuevo
vuelve a: (1) parsear con yaml los shards de aristas de cada store (`compose_edges_documents`,
`_cached_shard` + `model_copy(deep=True)` por shard), (2) componerlos y (3) volver a parsearlos
en `live_stale` (otra pasada por todos los shards, en cada lectura del índice).
Perfil en el layout (deskops origin/main d120766d, spec2viz/scion construidos, sldb sin construir):
- `sldb views run board` 7,5 s caliente; el índice con enlazados ~5,6 s bajo cProfile.
- Solo el store local ya cuesta ~2,6 s por proceso (1074 yaml.load, 1538 `_cached_shard`, ~1/3 en deepcopy).
- `deskops view board` (10,9 s) hace 5 `load_edge_index` por corrida: uno de `run_view` y cuatro de
  `show_task`/`transition_findings`/closeout (include_linked=False, claves distintas), no solo `run_view`.
- Un acierto en memoria cuesta aun 0,36 s (el `live_stale` vuelve a leer los shards).

## Benchmark (h1) `tests/perf/h11_bench_run_view.sh`
Arma el layout en /dev/shm (worktrees en el tip de origin de deskops, spec2viz, pron, scion; sldb = el
checkout dado), construye spec2viz, scion y deskops (el store sldb enlazado no se construye: sus
documentos de símbolos son generados y no están en git; construirlo tardó >20 min), mide 3 corridas
frío/caliente en proceso nuevo y da la mediana. "Frío" = sin ninguna caché de disco: sin store construido
la vista falla rápido ("Unknown view", H12), así que ese número no mide trabajo; la medida útil es el caliente.

### Línea base (b965c62d, carga 7,0 al medir)
| caso | frío (mediana de 3) | caliente (mediana de 3) |
|---|---|---|
| deskops view board | 2,84 s | 10,88 s |
| sldb views run board | 2,50 s | 7,52 s |

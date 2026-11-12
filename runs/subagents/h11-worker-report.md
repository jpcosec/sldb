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

## Cambio (commits H11)
- h2 `api/views/view_links.py`, `view_reading.py`: `run_view` abre el índice del store que llama (`include_linked=False`) y lo
  amplía (`widen`) solo si una sección tiene `include_linked` verdadero o `ref`/`prefix` con alias de enlace (params ya
  sustituidos), si hay `edges`/`transitions` y el índice local trae una referencia declarada sin resolver cuyo prefijo es un
  alias de enlace, o si la ViewDoc solo la trackea un enlazado (H9). Verificado en las ViewDocs semilla de deskops: ni
  `board` ni `task` usan `include_linked` ni `ref`/`prefix`; con los datos reales no hay referencias a enlaces, así que no amplían.
- h3 `store/edge_index/composed_disk.py`, `composed_reading.py`, `live_stale.py`: el índice compuesto (y los «hechos» de
  `live_stale`: stat/hash/contrato por documento) se guarda en `<store>/.sldb_cache/composed/<petición>.json` (JSON, nunca
  pickle: una caché de un clon no puede ejecutar código). Clave: `shards_signature` de cada store federado (sin el contador
  de rebuilds del proceso), mtimes de `core/documents`, versión del índice, `include_linked`, tags excluidos y el sello de
  contrato de cada modelo (`contract_signature`, `__doc_anchors__`, `__contract__`, porque los estados de ancla dependen
  de la clase). Cualquier diferencia = fallo y se compone como antes. `live_stale` sigue corriendo en cada lectura, ahora sobre
  los hechos guardados en vez de re-parsear todos los shards. `compose_edges_documents(copy=False)` evita los deepcopy en `live_facts`.
- `ViewReading.project()` releía `store.yaml` por fila cuando no hay project graph (11 yaml.load, 1,3 s bajo perfil): ahora lee una vez.
- h4 no se hizo (ver abajo).

## Desvíos
- Clave de h3: usé la firma de shards que ya es la clave de `_COMPOSED` (`shards_signature`) más los directorios de
  documentos, no la de `_stale_documents`/`documents_hash`: esa última exige leer los shards de documentos (el costo que se
  quiere evitar). Es mtime/size: dos escrituras de otro proceso en el mismo tick del reloj del FS no se distinguen (el
  contador en proceso que cubría eso no cruza procesos).
- Un store con documentos `stale` (p. ej. un enlazado sin construir) también se guarda; al leerlo se repite el marcado
  `documents_dirty` (inocuo en un proceso nuevo, que no tiene línea base).
- El store sldb enlazado no se construye en el benchmark (ver arriba); el layout también movió deskops de d120766d a 4904ddfe
  entre la línea base de la repro y esta corrida, por eso la línea base se remidió sobre el mismo layout (tabla).
- Revisión (6): el test fija que la revision de una vista sin `include_linked` no se mueve con un cambio en el enlazado y la de
  una con `include_linked` sí. La firma de shards de la revision sigue siendo la del store que llama.

## Casos probados (mediana de 3, proceso nuevo, carga 11-13 al medir; layout deskops 4904ddfe, sldb 69f56101, spec2viz b16c021, pron 7f2e308, scion 4ead6d0bf)
| caso | antes (b965c62d) | después |
|---|---|---|
| sldb views run board, store construido, caché de composición caliente | 7,0 s (7,5 s en la corrida anterior) | **1,59 s** |
| sldb views run board, primera corrida tras build (compone y guarda) | 7,0 s | 3,9 s |
| deskops view board, caliente | 11,97 s (10,9 s con d120766d) | **4,94 s** |
| deskops view board, primera corrida tras build | ~12 s | 11,3 s (≈ igual: compone una vez y guarda) |
| sin store construido / sin ninguna caché (frío) | 2,5 s / 2,8 s (falla rápido, H12) | 2,6 s / 2,9 s |

No se alcanzó «menos de 1 s». Lo que queda en `sldb views run board` (1,4 s medidos sin perfil): ~0,55 s de importar
`sldb.api`, ~0,38 s de leer el JSON del índice y revisar los archivos, ~0,35 s de `select_documents` (parsea ~540 shards
de documentos en yaml, `store/io/documents_index.py`), el resto es la propia vista. Eso sería h4/otra caché (los shards de
documentos); no lo hice: la disposición lo deja para cuando h2+h3 medidos no alcancen y el costo/riesgo es otro (invalidación
de otro índice). Lo digo como pendiente para que el coordinador decida.

## Suite
186 archivos `tests/**/test_*.py`, cada uno en su pytest desde /dev/shm/sldb-h11: todos verdes (5 archivos con solo skips:
test_anchors, test_machine_editor_schema, selfdoc/test_fingerprints, test_treesitter_agreement, test_treesitter_symbols).
`tests/test_clean_code_rules.py` 963 passed. `tools/check.sh --fast`: TODAS LAS PUERTAS PASAN.
Tests nuevos: `tests/api/test_run_view_reads.py` (5).

## Hipótesis para el resto del ecosistema
- deskops: `deskops view board` queda en ~4,9 s por trabajo propio: 3 × `show_task` (transition_findings, closeout con
  `build_closeout_graph_context`, `desk_graph` → ProjectGraph ~2 s) por tarjeta, y 31 `open_store` → `migrate_store_layout`
  → `_already_canonical` (≈1,3 s bajo perfil, 16 000 `Path.resolve`) en cada llamada. Candidatos: memoizar `open_store`/migración
  en sldb (`store/migration.py`, fuera de mi lista de archivos) y compartir un snapshot entre tarjetas en deskops.
- `rule_graph` carga el índice con enlazados (`rule_graph.py:101`) cuando el store tiene reglas enlazadas: es otro consumidor
  de `include_linked=True` que ahora se beneficia de la caché de disco, pero no del criterio de h2.
- sldb: `stores build` podría dejar `composed/` ya escrito (hoy la primera lectura lo hace).

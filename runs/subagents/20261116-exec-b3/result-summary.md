# Resultado — executor deskops-e-884be32362ef

Task: `task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3`
Resultado: **LISTO, rc 0**. Todos los comandos de Validation pasan (la salida completa está en `validation.log`).

## Qué cambió (archivo y función)

- **`src/sldb/store/graph/analysis/path_steps.py`** (nuevo; el Scope e Implementation Path lo autorizan y el coordinador lo confirmó):
  - `explain_path(index, nodes, relations, directed)` arma `{"path", "steps"}` con un step `{source, target, edges}` por cada par consecutivo de nodos.
  - `explained_path` envuelve a `path_between` y `explained_paths` a `paths_between`.
  - Funciones privadas `_edges`, `_item`, `_provenance` y `_rank`.
  - Cómo se forma `edges`:
    - Se leen las aristas `a->b` con `index.edges_from(a)` y, si el recorrido no es dirigido, las `b->a` con `index.edges_from(b)`. Las dos se filtran por `analysis.relations.resolve`.
    - Una arista sin `reverse` va `forward` si sale de a y `backward` si sale de b.
    - Una arista espejo (`metadata.reverse` true) se emite con la dirección opuesta y con la misma metadata que su arista directa. Al deduplicar queda como esa arista directa `backward`, nunca por separado.
    - Orden: relation_doc > schema > structural > alias, y un origin desconocido al final. Los empates se ordenan por relation y luego por relation_doc o field.
    - `provenance` lleva solo `origin`, `relation_doc` (si origin es relation_doc), `field` (si origin es schema) y `from_store`. Las claves ausentes no se emiten, y `evidence`, `condition`, `axis` y `attributes` quedan fuera.
- **`src/sldb/store/graph/backend/networkx_backend.py`**: `_OPERATIONS` suma `path_explained` y `paths_explained`. `path` y `paths` no cambian.
- **`src/sldb/api/graph/analyze.py`**: `graph_path` y `graph_paths` ganan `explain: bool = False`, que elige la operación y va después de `backend`. Con explain=False la forma es la de siempre.
- **`src/sldb/cli/parsers/graph_analysis.py`** (`_add_path`): agrega el flag `--explain`.
- **`src/sldb/cli/commands/graph_path_print.py`** (nuevo, autorizado por el Scope): `print_path(args, backend, relations, index)` es todo el handler de `sldb graph path`, con y sin `--all` y con `--explain`. Imprime JSON igual que el resto de los comandos.
- **`src/sldb/cli/commands/graph_analysis.py`**: `GraphAnalysisCLI._path` delega en `print_path`, y se sacan los imports de `graph_path` y `graph_paths`. El archivo baja de 70 a 64 líneas efectivas.
- **`src/sldb/cli/serve/graph_routes.py`** (`path_payload`): con `?explain=1` (o `true`) devuelve `{"path", "steps"}`. Sin el parámetro la respuesta sigue siendo `{"path": [...]}`.
- **`tests/api/test_api_graph_analysis.py`**: 4 tests nuevos.
  - Explain sobre AnalysisWorld: forward y backward, `graph_paths` con explain, y la forma sin explain intacta.
  - Precedencia, espejo como backward, `from_store`/`field`, origin desconocido al final, `evidence` excluida y modo dirigido.
  - CLI `--explain` y `path_payload` con y sin `explain=1`.
  - El índice del propio repo: `ritual-execution → ritual-testing → ritual-closeout`, con origin y relation_doc en cada arista.
- **`CHANGELOG.md`**: entrada en 0.1.13.

## Done When

- **Comandos de Validation**: los 6 pasan con rc 0.
  - `test_api_graph_analysis` 10 passed
  - `test_graph_analysis` 16 passed
  - `test_graph_backend` 9 passed
  - `test_serve` 61 passed
  - `test_clean_code_rules` 1173 passed
  - `check.sh --fast`: TODAS LAS PUERTAS PASAN
- **`graph_path(..., explain=True)` sobre el índice del repo**: lo cubre `test_explain_over_the_repo_own_index_names_origin_and_relation_doc`. Store `<repo>/.sldb` con `include_linked=False`. Los tramos traen `origin: relation_doc` y `relation_doc` (`execution-task_activates`, `testing-task_hands_to_closeout`).
- **Goldens**: `tests/fixtures/graph_goldens/` sin cambios (`git status` limpio ahí), y `test_graph_backend` pasa.
- **Exposición**:
  - `sldb graph path --explain` lo cubre `test_the_cli_and_serve_expose_the_explained_path`.
  - `GET /graph/path?explain=1` lo cubre el mismo test, llamando a `path_payload` con un handler simulado.
- **CHANGELOG**: hecho.
- **Commit**: no lo hice, porque el brief prohíbe `git commit`. Queda para el integrador o el closeout.
- **Aviso a IR**: lo manda el coordinador al cerrar, según su aclaración. Texto sugerido: «sldb.api.graph.graph_path/graph_paths aceptan explain=True: {path, steps[{source,target,edges[{relation,direction,provenance{origin,relation_doc|field,from_store}}]}]}; CLI `sldb graph path --explain`, serve `/graph/path?explain=1`».

## Comandos corridos (rc)

- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py` → 0
- `... pytest -q tests/store/test_graph_analysis.py` → 0
- `... pytest -q tests/store/test_graph_backend.py` → 0
- `... pytest -q tests/test_serve.py` → 0
- `... pytest -q tests/test_clean_code_rules.py` → 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` → 0. Omite la puerta de afirmaciones con `--fast`.
- Extra: `python tools/check_claims.py CHANGELOG.md` dice FAIL con 3 afirmaciones falsas: `docs/missing`, `docs/ambiguous` y `sldb query`. Las tres **ya estaban en el CHANGELOG de HEAD** y no vienen de esta entrada; todas las rutas que nombra la entrada nueva existen.
- No corrí ni la suite completa ni `sldb stores build --check`; quedan delegados al integrador.

## Archivos tocados (lista exacta)

- CHANGELOG.md
- src/sldb/api/graph/analyze.py
- src/sldb/cli/commands/graph_analysis.py
- src/sldb/cli/commands/graph_path_print.py (nuevo)
- src/sldb/cli/parsers/graph_analysis.py
- src/sldb/cli/serve/graph_routes.py
- src/sldb/store/graph/analysis/path_steps.py (nuevo)
- src/sldb/store/graph/backend/networkx_backend.py
- tests/api/test_api_graph_analysis.py

## Desvíos e incidentes

- **Incidente en `.sldb/`, ya revertido**: mientras buscaba cómo abrir el store del repo pasé `--store .sldb/core`, una vez con `load_edge_index` en una sonda y otra con `sldb graph central`. Las dos lo trataron como raíz de store y migraron el layout:
  - movieron `.sldb/core/store_index.yaml` a `.sldb/core/core/store_index.yaml`, reescribiendo los `models_index` a `core/core/models/...`;
  - crearon `.sldb/core/core/models/*.yaml` vacíos.

  Restauré `.sldb/core/store_index.yaml` desde ese archivo, revirtiendo solo los `models_index` a `.sldb/core/models/...`, y borré `.sldb/core/core/`. Comprobaciones:
  - el diff contra HEAD vuelve a ser solo la línea `store_hash` del inicio;
  - `hash_models_layer` sobre los modelos actuales da exactamente ese `store_hash` (`b780a36c…`);
  - `git status .sldb` coincide con el del arranque.

  Nada más dentro de `.sldb/` cambió (lo verifiqué con mtimes). Para el futuro: el store del repo se abre con la ruta absoluta a `<repo>/.sldb`; `.sldb/core`, `.` y `.sldb` relativo fallan o migran.
- **Orden de los parámetros**: `explain` va después de `backend`, que estaba antes en las firmas, así que no rompe ninguna llamada posicional existente.
- **`directed=True`**: el contrato no lo precisa para las aristas `backward`. Solo se listan las aristas `a->b` del grafo dirigido; un espejo `a->b` aparece como su arista directa `b->a` `backward`, porque eso fue lo que recorrió el camino.
- **Pills**: ninguno atado, así que no hay choque con el contrato.

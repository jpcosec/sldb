# H9 — informe del worker (task.debug)

Tarea: `desk/tasks/task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz.md`.
Rama `wt/h9-linked-views`, base origin/main `23e4c2b2`.

## Reproducción

`~/proyectos/SLDB_1/coord2-ccconfig/cc34/h9-repro/h9_repro.py`: store A enlaza a B (`link_store(a, b, name="B")`),
la ViewDoc `probe` vive solo en B. `run_view(B, "probe")` funciona; `run_view(A, "probe")` da
`SLDBDocumentTargetError: Unknown view: probe`. En el índice compuesto de A el nodo es
`sldb://document/B:ViewDoc:probe` con `semantics = {export_id: ViewDoc:probe, path: views/probe.md, store: B}`
e `index.node("ViewDoc:probe")` es None.

## Causa raíz (src/sldb/api/views/list_views.py, base 23e4c2b2)

1. **Resolución por id local.** `load_view` busca `f"ViewDoc:{name}"` en el índice. La federación
   (`store/edge_index/federation.py::qualify_id`) nombra los documentos de un store enlazado
   `<link>:Model:name`, así que una ViewDoc enlazada nunca coincide: `read_view` levanta `Unknown view`.
2. **Archivo leído desde la raíz equivocada.** `read_view` une `node.semantics["path"]` (relativo a la raíz
   del store que trackea el documento) con `open_store(store_path).project_root`, la raíz del store LOCAL.
   Aunque (1) encontrara el nodo, leería `A/views/probe.md`, que no existe (o, peor, otro archivo de A con
   esa ruta). Además lo lee con `.read_text()` sin la guarda de lectura (`sldb.store.source_read`):
   sigue symlinks y rutas que salen de la raíz.
3. **Catálogo solo local.** `list_views` compone el índice con `include_linked=False`, así que las ViewDoc
   enlazadas no se listan.
4. (derivado) `view_revision.content_hash` lee el shard de la ViewDoc del store local: para una enlazada
   daría `""` y la `revision` no se movería cuando la ViewDoc cambia en B.

El dato que falta ya está en el nodo: `_merge` de `compose.py` sella cada nodo con
`facets.source.store_path`, el `.sldb` del store que lo aporta (local o enlazado).

## Arreglo (v1-v5)

- **v1 resolución** — `src/sldb/api/views/view_source.py::view_node`: primero `ViewDoc:<name>` local; si
  no, la única ViewDoc enlazada con ese nombre; `<link>:<name>` nombra una enlazada directamente. Dos o más
  enlazadas: `SLDBDocumentTargetError('Ambiguous view: <name> (linked in <s1>, <s2>)')`, sin elegir.
- **v2 archivo** — `read_view_node`: la raíz es `project_root(facets.source.store_path)` del nodo (el store
  que lo trackea). Lee por la guarda que ya está en main (`sldb.store.source_read`: `unreadable_reason` +
  `read_source_text` con `O_NOFOLLOW`); fuera de la raíz o symlink = error que lo nombra, no se lee. No hizo
  falta el TODO(task-seguridad-live-stale).
- **v3 list_views** — compone con `include_linked=True`; lista locales y enlazadas; una enlazada que comparte
  nombre con otra vista se lista `<link>:<name>` (y `run_view` acepta ese nombre).
- **v4 evaluación** — sin cambio de mecanismo: las secciones ya seleccionan sobre `reading.store_path`
  (el store que llama). El test lo fija (B tiene su propio `Note:b1` y no aparece en las filas).
- **(derivado) revision** — `view_revision.revision` recibe el nodo de la vista y lee su `content_hash` del
  shard del store que la trackea; editar la ViewDoc en B mueve la revision de A.
- `load_view(name, index) -> (ViewDoc, nodo)`; `run_view` usa el nodo para la revision. `serve` no se tocó:
  `GET /views` y `/views/<name>` heredan el arreglo; la ambigüedad sale 404 como cualquier
  `SLDBDocumentTargetError`.
- **v5 tests** — `tests/api/test_views_linked.py` (6): enlazada encontrada, leída desde B (un señuelo en
  `A/viewdoc/board.md` no se lee) y evaluada sobre A; `list_views(A)`; ambigüedad nombrada y listado
  calificado; la local gana; la revision se mueve al editar la vista en B; un symlink fuera de la raíz no se
  lee. Los 6 fallan en la base y pasan con el arreglo.
- Docs: `docs/architecture/views.md` §A view from a linked store; CHANGELOG 0.1.13.

## Desvíos

- `contracts/layers.toml` (fuera de la lista de files, permitido por el brief para grados medidos): la arista
  nueva vistas_compuestas → lectura_de_fuentes sube `nucleo.needed_by` 46→47 y `operacion.needs` 68→69, con
  comentario fechado. Sin eso, la puerta `ejes` de `check.sh --fast` falla; con la base en PASS.
- Este informe vive en `runs/subagents/` (convención del informe de livestale).

## Validación (worker)

Tests de a uno con la guarda pgrep y systemd-run MemoryMax=2G:

- tests/api/test_views_linked.py — 6 passed
- tests/test_clean_code_rules.py — 955 passed
- tests/api/test_views.py — 17 passed
- tests/api/test_view_doc.py — 22 passed
- tests/notations/test_notation_view_and_routes.py — 9 passed
- tests/notations/test_notation_models_and_builtins.py — 15 passed
- tests/test_serve.py — 61 passed
- tests/store/test_live_stale_security.py — 8 passed
- `bash tools/check.sh --fast` — PASS (núcleo aislado, capas, identidad, ejes, superficie)
- Reproducción de CC34 (`h9_repro.py`) con `PYTHONPATH=src`: `run_view(A, "probe")` ya no levanta.

Los 7 pasos del workflow de sldb en clon limpio: los corre el coordinador.

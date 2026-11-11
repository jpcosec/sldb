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

## Arreglo

(se completa tras implementar)

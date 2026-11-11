# livestale-worker: informe (SEGURIDAD live_stale)

Rama `wt/livestale-security`, base `9c9dac6b`. Contrato: TaskDoc
`task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-...` (task.debug) y la disposición
de pi en el brief del coordinador.

## Causa raíz

Reproducción del coordinador (sldb 9c9dac6b): un desk de prueba con dos documentos trackeados;
uno se reemplaza por un symlink a `/dev/shm/outside-secret/secreto-externo.md`. Un proceso nuevo
llama `sldb.api.edges.edge_reading.load_edge_index(.sldb, include_linked=False)` con un audit
hook de `open`: abre 26 `.md`, entre ellos el archivo de fuera de la raíz a través del symlink.

Cadena, en el código de 9c9dac6b:

1. `load_edge_index` -> `compose.compose_edge_index` -> `compose._with_live_stale`, en **cada**
   lectura del índice (el índice compuesto se cachea; `live_stale` no).
2. `live_stale.live_stale(store_path, ...)` recorre todos los modelos y, por cada documento
   trackeado con shard, llama `_moved(shard, ..., root / entry.path, ...)`.
3. `_moved` llama siempre `_file_hash(path)`, que hace `path.stat()` (sigue symlinks) y
   `path.read_text()` (abre y sigue symlinks). No hay ninguna comprobación de que
   `path.resolve()` quede dentro de `project_root(store_path)`, ni de que la entrada no sea un
   symlink: `root / entry.path` con un symlink en el último componente (o en un directorio
   intermedio) apunta adonde diga el symlink.
4. El único freno era `_FILE_HASHES`, un caché **por proceso** indexado por (mtime_ns, size):
   un proceso nuevo (un servidor que arranca, graph_ui, un CLI) no tiene nada y lee y hashea
   **todos** los archivos trackeados, cambien o no.
5. El shard (`DocEdges`) solo guarda `source_hash`; no guarda nada barato (un stat) con lo que
   decidir "este archivo no se movió" sin leerlo. Por eso el diseño de GO04 (d7eefdeb, "EdgeIndex.stale
   ve la edición externa") necesitaba leer cada archivo para ver una edición externa.

Consecuencias: (a) leer el índice abre archivos fuera de la raíz a través de symlinks
trackeados, antes de que un consumidor (graph_ui) pueda aplicar sus guardas; (b) abre todos los
archivos protegidos de un consumidor aunque no hayan cambiado; (c) coste O(bytes del proyecto)
por proceso nuevo.

`stores check` (`store/diagnostics.py: _diagnose_doc`, `field_set_drift.document_drifted`)
tiene la misma forma: `doc_path.read_text()` sin guarda de raíz ni de symlink. Ahí se reportan
los hallazgos nuevos (`store/path-outside-root`, `store/symlink-not-read`).

## Arreglo

_(pendiente: se completa con el arreglo)_

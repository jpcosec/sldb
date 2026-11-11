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

## Arreglo (s1-s3)

- **Guarda** (`src/sldb/store/hashing.py`: `unreadable_reason`, `source_stat`,
  `read_source_text`). Raíz = `project_root(store_path)`. Solo `lstat` y `resolve`, nunca un
  open: una ruta cuyo `resolve()` no queda bajo `root.resolve()` es `outside-root` (s1: un
  symlink que escapa, un directorio del camino que escapa, un symlink colgante hacia afuera);
  una ruta que es symlink dentro de la raíz es `symlink` (s2). La lectura usa `O_NOFOLLOW`,
  así que un archivo cambiado por un symlink entre la guarda y el open tampoco se sigue. Vive en
  `hashing.py` (eje `identidad_y_hash`) y no en un módulo nuevo porque un archivo nuevo pide eje
  en `contracts/layers.toml`, que no está en los files permitidos.
- **live_stale** (s1-s3): si la guarda dice que no, el documento es stale sin leerlo. Si el
  `lstat` coincide con `DocEdges.source_stat`, no se abre. Solo un archivo cuyo stat cambió se
  lee y se hashea (y el hash se cachea por proceso como antes). `stale` sigue siendo
  `list[str]`; el motivo va en el hallazgo.
- **Stat en el shard** (`DocEdges.source_stat: list[int] | None = None`). Lo escribe
  `edge_doc_contribution.sync_doc_shard`: en un shard nuevo, y en uno reutilizado cuyo stat
  falta o cambió. Solo se estampa si el archivo pasa la guarda y su texto da el `source_hash`
  de la entrada (stat, lectura, stat otra vez, iguales): una edición externa anterior al build
  no se marca como vigente. Un shard sin el campo se hashea como hoy. Para que "el próximo
  build lo complete" de verdad (el walk por modelo se salta con el caché), `edge_sync` guarda la
  línea base del walk como `contract_hash + "|source_stat"`: un store construido antes recorre
  una vez cada modelo comparando todos sus documentos, sin cambiar `EDGE_INDEX_VERSION` ni el
  contrato de ningún shard. `.sldb_cache/` no entra en `stores build --check`, así que un mtime
  en el shard no rompe esa comparación.
- **Hallazgos** (`stores check`): `DiagnosisNote.PATH_OUTSIDE_ROOT` / `SYMLINK_NOT_READ`,
  códigos `store/path-outside-root` y `store/symlink-not-read` en `store_findings._DOC_CODES`,
  nivel alert. Necesitan decisión (`NEEDS_DECISION`) y cuentan como dañados. `stores check`
  tampoco los lee: `diagnostics._diagnose_doc` y `field_set_drift.document_drifted` pasan por
  la guarda y leen con `O_NOFOLLOW`; para esas rutas no se consulta el historial git.
  `src/sldb/api/stores/store_findings.py` está fuera de la lista literal de files, pero lo
  nombra la disposición de pi.

### s2: ¿rompe un caso real?

No encontré un caso real que dependa de trackear un symlink. En `src/` el único symlink es el
que `stores build --check` crea para un store enlazado; `project_root` lo resuelve y las rutas
de sus documentos quedan dentro. En los stores de sldb, deskops, pron, spec2viz y scion ningún
shard de documento tiene `path` absoluto ni con `../` (los que aparecen son rutas de modelos).
El único repo con symlinks en git es scion (`GEMINI.md`, `claude.md` -> `AGENTS.md`), y no
están trackeados en su store. Si un consumidor
lo hiciera, ahora vería el documento stale y la alerta `store/symlink-not-read`. Sigue
leyéndose en `docs show` y en la reconstrucción, que están fuera de esta tarea.

## Fuera de alcance (s6 y lo visto al pasar)

- a2 de la nota (rebuild no resuelve la stale de una edición externa; stale global): sin tocar.
- La reconstrucción (`edge_rebuild._doc_edges`, payload) y el track (`store/ops.py`) siguen
  leyendo por la ruta trackeada sin esta guarda. `sldb.api.check_store` también corre
  `scan_rewrite_loss` y `structural_noise` (en `src/sldb/api/stores/`), que leen documentos sin
  la guarda. Para cerrar esos caminos hace falta una tarea aparte (files fuera de esta).
- Un archivo tocado sin cambiar su texto (stat nuevo, mismo hash) se lee una vez por proceso
  hasta que su shard se reconstruye: `rebuild_edges` no lo marca sucio.
- Como antes con `_FILE_HASHES`, una edición que conserva tamaño y cae en el mismo `mtime_ns`
  no se ve sin reconstruir.

## Servidores (s5)

- `sldb serve` (`src/sldb/cli/commands/serve.py`) es `ThreadingHTTPServer((args.host,
  args.port))` y `--host` vale `127.0.0.1` por defecto (`cli/parsers/serve.py:11`). No hay
  otro camino que escuche (grep de `ThreadingHTTPServer`, `socketserver`, `bind`, `listen`,
  `0.0.0.0` en `src/`): **nada escucha fuera de localhost por defecto.** El token bearer es
  opcional y viene apagado (`cli/serve/auth.py`).
- Usa `load_edge_index` directo en `cli/serve/similar_routes.py:28` e indirecto en las rutas de
  grafo, aristas, vistas, reglas y proyecto (`sldb.api.graph.*`, `sldb.api.edges.*`,
  `run_view`, `rule_graph`). Antes del arreglo, cada petición pasaba por `live_stale`, y en el
  proceso del servidor la primera abría todos los `.md` trackeados, siguiendo symlinks.

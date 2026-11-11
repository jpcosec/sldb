# secrest-worker: SEGURIDAD (resto), toda lectura de un documento trackeado pasa por la guarda

Rama `wt/secrest`, base origin/main `7b9b1e6d`. Contrato: TaskDoc
`task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores`
(task.debug). Files sumado por el coordinador: `src/sldb/cli/commands/stores_build_check.py`.

## 1. Reproducción (sobre 7b9b1e6d, antes del arreglo)

Desk de prueba en /dev/shm con un modelo `Memo`, tres documentos `a.md`, `b.md`, `c.md` trackeados
y declarados en `store.yaml`; `b.md` reemplazado por un symlink a `/dev/shm/secrest-repro/outside/secret.md`
y `new.md` un symlink relativo a `../outside/c-secret.md`. Cada comando corre con un audit hook de
`open` que imprime la pila sldb de cada `.md` abierto fuera de la raíz.

| comando | abre el archivo de afuera | por dónde |
|---|---|---|
| `stores check` | sí | `store/query.py:26` (carga runtime), `api/stores/scan_structural_noise.py:33`, `api/stores/scan_rewrite_loss.py:21` |
| `stores update` | sí | `api/stores/index_refresh.py:82`, `store/semantic_doc_tags.py:26`, `store/section_rebuild.py:73`, `store/edge_rebuild.py:67` |
| `stores build` | sí | `api/stores/index_refresh.py:82` (vía `update_store_indexes`) |
| `stores build --check` | sí | `cli/commands/stores_build_check.py:94` (`is_file()` + `shutil.copy2` siguen el enlace al copiar a la scratch) y, en la copia, `store/ops.py:28` y las mismas del rebuild |
| `docs update b` | **sí, y escribe**: el archivo de afuera quedó reescrito con el payload | `api/documents/provenance_stamp.py:31` (lee), `api/documents/payload_save_steps.py:90` (escribe), y las del rebuild |
| `docs track new.md` | sí, y lo trackea | `api/documents/track_document_file.py:64,46,47`, `store/ops.py:28`, y las del rebuild |

Con el modelo `TaskCodeDoc` del coordinador el contenido de afuera no valida y los comandos terminan en
`Unexpected: 2 validation errors`; con `Memo` el secreto valida y se lee, se hashea y se indexa sin aviso.

## 2. Causa raíz

La guarda `sldb.store.source_read` (`unreadable_reason` + `read_source_text` con `O_NOFOLLOW`) se
introdujo en la tarea live_stale para la lectura del índice de aristas (`edge_index/live_stale.py`,
`edge_doc_contribution.built_stat`), el diagnóstico de `stores check` (`diagnostics.py`) y
`field_set_drift.py`. Cada otra lectura del texto de un documento trackeado arma `root / doc.path` y
llama `read_text()` (o `codec.extract(..., read_text())`) directamente: `Path.read_text`, `exists()`,
`is_file()` y `shutil.copy2` siguen symlinks, de modo que un path trackeado que es symlink (o que
cruza un directorio symlink) lee, hashea, extrae, secciona, etiqueta y, en `docs update`, **escribe**
fuera de la raíz. No había un único punto de apertura: la guarda era opcional para cada lector.
`docs track` además resuelve el path (`_resolve_path` → `.resolve()`) antes de cualquier chequeo, así
que el symlink se pierde y se trackea el destino.

## 3. Inventario (grep de `read_text`/`read_bytes`/`open` en los files de la tarea)

Criterio de documento: el de sldb, un path que está trackeado (fila de un documents index) o que
recibe `docs track` o que nombra un include de `store.yaml`. Alcance: toda lectura de su texto para
extraer, hashear, seccionar o etiquetar.

| archivo:línea (7b9b1e6d) | lectura | antes | después |
|---|---|---|---|
| api/stores/index_refresh.py:82 | rehash de `stores update`/`build` | `read_text` sin guarda | `unread_documents.tracked_text` (index_refresh.py:79 → unread_documents.py:49-55): `warn_unread` nombra el hallazgo, `name (code)` en `skipped_documents`, después `read_source_text` |
| api/stores/scan_rewrite_loss.py:21 | extracción en `stores check` | `read_text` sin guarda | `guarded_text` (scan_rewrite_loss.py:21) |
| api/stores/scan_structural_noise.py:33 | texto en `stores check` | `read_text` sin guarda | `guarded_text` (scan_structural_noise.py:34) |
| store/ops.py:28 | hash al trackear | `read_text` sin guarda | `read_source_text` con `O_NOFOLLOW` (ops.py:29); el rechazo va antes, en `track_document_file` (ver decisión 2) |
| store/query.py:26 | extracción runtime (`load_runtime_documents`) | `read_text` sin guarda | `guarded_text`; no leído = sin documento runtime, como uno que falta (query.py:24) |
| store/section_rebuild.py:73 | secciones | `read_text` sin guarda | `unreadable_reason` en `section_sync._sync_one_section` (section_sync.py:59) + `read_source_text` (section_rebuild.py:74) |
| store/semantic_doc_tags.py:26 | etiquetas | `read_text` sin guarda | `unreadable_reason` en `semantic._readable` (semantic.py:79) + `read_source_text` (semantic_doc_tags.py:27) |
| store/edge_rebuild.py:67 | payload para aristas | `read_text` sin guarda | `guarded_text` en `read_payload` (edge_rebuild.py:68) |
| api/documents/track_document_file.py:46,47,64 | round-trip, ruido, frontmatter de `docs track` | `read_text` tras `.resolve()` | `refuse_unreadable` sobre el path sin resolver (track_document_file.py:55) + una sola `read_source_text` (:46) |
| api/documents/provenance_stamp.py:31 (+ payload_save_steps.py:90 escribe) | provenance previa en `docs update`/save | `read_text`/`write_text` sin guarda | `refuse_unreadable` antes de leer y escribir (payload_save_steps.py:89); `read_source_text` (provenance_stamp.py:32) |
| api/documents/document_serialization.py:20 | provenance de un documento | `read_text` sin guarda | `guarded_text` (document_serialization.py:21) |
| api/documents/document_ast.py:22 | AST de un documento | `read_text` sin guarda | `read_source_text` tras `runtime_document`, que ya pasa por `store.query` guardada (document_ast.py:23) |
| api/documents/replace_text.py:76 | `replace_text` | `read_bytes` sin guarda | `refuse_unreadable` antes de `_read` (replace_text.py:46); `read_bytes` (:78) solo tras el rechazo |
| cli/commands/stores_build_check.py:94 (sumado) | copia de fuentes a la scratch | `is_file()` + `copy2` siguen el enlace | `is_symlink() or is_file()` + `copy2(..., follow_symlinks=False)` (stores_build_check.py:92-94); en la copia, `apply_includes` no trackea el symlink (apply_declaration.py:71) y `build_store['unread']` lo nombra como `copy: <path>` |
| store/diagnostics.py:55 | diagnóstico de `stores check` | ya guardada (live_stale) | sin cambio |
| store/field_set_drift.py:47 | drift de campos | ya guardada | sin cambio |
| store/edge_index/live_stale.py:77, store/edge_doc_contribution.py:77 | índice de aristas | ya guardadas | sin cambio |

Excepciones del grep (no son documentos trackeados): `store.yaml` (api/stores/store_declaration.py:74),
`store_index`/models/documents/sections indexes y shards yaml (store/io/*.py, migration_*.py,
semantic_dag.py, semantic_index.py), caches json (scan_cache.py, runtime_cache_disk.py, built_cache.py,
graph_io.py), `pyproject` (store/package_version.py:17), `.gitignore` (api/stores/gitignore_lines.py:59),
semillas del scaffold (api/stores/scaffold_sources.py, scaffold_store.py:70), el snapshot de rollback
(store/io/rollback.py:44, restaura lo que la transacción escribe), `transaction_ops.write_file` (archivo
plano, no documento) y el lock (store/io/lock.py).

## 4. Arreglo (r1-r5)

- **Un punto de apertura** (`sldb/store/source_read.py`): `guarded_text(root, path)` da el texto o
  `None` (falta, o `unreadable_reason` dice que no); `refuse_unreadable(root, path)` levanta
  `SLDBStoreError` antes de abrir. Toda lectura de la tabla usa `read_source_text` (`O_NOFOLLOW`).
- **Hallazgo nombrado, sin abortar** (`sldb/api/stores/unread_documents.py`, eje de api/stores):
  `unread_finding` arma la alerta con `store_findings._DOC_CODES` y los textos de
  `document_verdicts` (los mismos de `stores check`; `unread_verdict.unread_note` mapea el motivo
  a `DiagnosisNote`). `warn_unread` la emite como warning; `tracked_text` la usa en el rehash de
  update/build (`name (code)` en `skipped_documents`); `unread_declared` da las alertas de los
  paths declarados para `build --check`. En el nivel store (secciones, semántica, aristas,
  consulta) un documento no leído se salta en silencio: no se puede importar api desde store, y
  check/update ya lo nombran.
- **track (r2)**: `track_document_file._resolve_path` llama `refuse_unreadable` sobre el path
  unido a la raíz y **sin resolver** (antes `.resolve()` perdía el symlink y trackeaba el destino).
- **Escritura**: `write_rendered_document` (docs update, save_document_payload) y `replace_text`
  rechazan un documento así antes de leer o escribir.
- **build --check** (file sumado): `is_symlink() or is_file()` y `copy2(..., follow_symlinks=False)`.
- **Límites (r5)**: `test_clean_code_rules` en verde sin subir límites (se partieron
  `track_document_file._refuse_unfit`, `semantic._readable`, y `tracked_text` salió de
  index_refresh a unread_documents). Grados medidos actualizados con comentario fechado en
  `contracts/layers.toml`: nucleo needed_by 46→49, persistencia needs 22→24, operacion needs 68→69.

## 5. Después (misma reproducción, rama wt/secrest)

| comando | abre el archivo de afuera | qué dice |
|---|---|---|
| `stores check` | no | `alert: [store/path-outside-root] Memo:b` (como antes, sin abrirlo en los escaneos) |
| `stores update` | no | `[warning] alert: [store/path-outside-root] Memo:b: ...`; `Skipped missing documents: b (store/path-outside-root), c`; exit 1 |
| `stores build` | no | el mismo warning; el resumen `built:` no cambia de forma |
| `stores build --check` | no | warning por el path declarado no trackeado y `alert: [store/path-outside-root] copy: b.md` |
| `docs update a` | no | `Updated 'a'` |
| `docs update b` | no, y no escribe | `.../b.md: the path resolves outside the project root; sldb neither reads nor writes it ...`, exit 1; el secreto queda intacto |
| `docs track new.md` | no | el mismo error, exit 1; un symlink dentro de la raíz: `... the path is a symlink; ...` |

## 6. Tests

- Nuevo `tests/store/test_tracked_reads_guarded.py` (9): audit hook de `open` en un proceso nuevo
  por comando; check, update, build y build --check no abren el symlink saliente, nombran
  `store/path-outside-root` y no dan `Unexpected`/`Traceback`; docs update de otro documento no
  lo abre; docs update del symlink se rechaza y no escribe afuera; docs track de un symlink
  saliente y de uno interno se rechaza sin abrirlo; update nombra `store/symlink-not-read`.
- De a uno, con la guarda de pgrep: todos los archivos de tests/store y tests/api (todos tocan
  las lecturas cambiadas por grep), más tests/test_linked_doc_refs.py, test_linked_structural.py,
  test_links_batch_cli.py, test_runtime_cache.py, test_serve.py y test_clean_code_rules.py:
  122 archivos. Primera pasada: 121 en verde y `test_stores_build.py` con 4 fallos (la clave
  nueva `unread` rompía el informe dorado de `build_store`, y `ops.track` rechazaba el documento
  fuera del proyecto que crea `create_document`). Corregido (decisiones 1 y 2, sección 8) y vuelto a correr de a uno
  los 70 archivos que pasan por track/create/ops/build (grep) más test_live_stale_security: todos
  en verde (test_machine_editor_schema.py: 7 skipped, como en main); `test_stores_build.py` 27 passed.
- `tests/store/test_live_stale_security.py` verde. `bash tools/check.sh --fast`: PASS.

## 7. Fuera de files (pendiente, para una tarea siguiente)

Lecturas del texto de documentos trackeados por `root / doc.path` sin la guarda, fuera de los
files de esta tarea y de los seis comandos cubiertos:
`api/model_registry/model_index_writes.py:63`, `api/edges/builtin_relation_writes.py:53`,
`api/edges/rewrite_references.py:84`, `api/edges/project_graph/document_metadata.py:24`,
`project_texts.py:32`, `declared_target_nodes.py:63`, `api/views/list_views.py:48`,
`api/records/ast_target.py:38`, `api/records/fields.py:52`, `api/records/iter_records_docs.py:35,44`,
`api/segments/build_document_segments.py:38`, `cli/serve/document_routes.py:62`,
`cli/commands/sections_show.py:27`, `links/render.py:15`, `links/recovery.py:14,28`,
`models/structured_doc.py:87`. Varias toman el documento de `load_runtime_documents`, que ya no
devuelve uno no leído, pero leen por su cuenta. `provenance_stamp.stamped_file` ahora abre con
`O_NOFOLLOW`: sus llamadores fuera de files (`model_drafts/backfill.py`,
`edges/builtin_relation_writes.py`) fallan con ELOOP ante un symlink en vez de seguirlo.

## 8. Decisiones revisables

1. **Forma del informe de `build_store` sin cambio**: no hay clave nueva; `stores build` nombra
   por warning (del rehash y de `apply_includes`, que no trackea un path declarado symlink), y
   `build --check` arma sus alertas con `unread_declared`. En `build --check` el warning sale dos
   veces porque `apply_includes` corre antes y después de los generadores.
2. **`create_document` a un path fuera del proyecto sigue trackeando** (spec2viz lo usa; lo
   cubre `test_a_document_outside_the_project_does_not_break_the_declaration`): el rechazo de r2
   vive en `track_document_file` (docs track, build, transacciones), no en `store.ops.track`, que
   lee con `O_NOFOLLOW`. `docs track` de un path absoluto fuera de la raíz, que antes se
   trackeaba, ahora se rechaza.
3. **`stores update` sale 1** con un documento no leído (va a `skipped_documents` como
   `nombre (código)`); el CLI lo imprime bajo "Skipped missing documents" porque
   `cli/commands/store_update.py` no está en files.
4. **TOCTOU**: escritura y `read_bytes` de `replace_text` siguen tras el rechazo sin
   `O_NOFOLLOW`; una carrera que cambie el archivo por un symlink entre el chequeo y la escritura
   no está cubierta.

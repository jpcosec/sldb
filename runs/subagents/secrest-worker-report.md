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
| api/stores/index_refresh.py:82 | rehash de `stores update`/`build` | `read_text` sin guarda | _pendiente_ |
| api/stores/scan_rewrite_loss.py:21 | extracción en `stores check` | `read_text` sin guarda | _pendiente_ |
| api/stores/scan_structural_noise.py:33 | texto en `stores check` | `read_text` sin guarda | _pendiente_ |
| store/ops.py:28 | hash al trackear | `read_text` sin guarda | _pendiente_ |
| store/query.py:26 | extracción runtime (`load_runtime_documents`) | `read_text` sin guarda | _pendiente_ |
| store/section_rebuild.py:73 | secciones | `read_text` sin guarda | _pendiente_ |
| store/semantic_doc_tags.py:26 | etiquetas | `read_text` sin guarda | _pendiente_ |
| store/edge_rebuild.py:67 | payload para aristas | `read_text` sin guarda | _pendiente_ |
| api/documents/track_document_file.py:46,47,64 | round-trip, ruido, frontmatter de `docs track` | `read_text` tras `.resolve()` | _pendiente_ |
| api/documents/provenance_stamp.py:31 (+ payload_save_steps.py:90 escribe) | provenance previa en `docs update`/save | `read_text`/`write_text` sin guarda | _pendiente_ |
| api/documents/document_serialization.py:20 | provenance de un documento | `read_text` sin guarda | _pendiente_ |
| api/documents/document_ast.py:22 | AST de un documento | `read_text` sin guarda | _pendiente_ |
| api/documents/replace_text.py:76 | `replace_text` | `read_bytes` sin guarda | _pendiente_ |
| cli/commands/stores_build_check.py:94 (sumado) | copia de fuentes a la scratch | `is_file()` + `copy2` siguen el enlace | _pendiente_ |
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

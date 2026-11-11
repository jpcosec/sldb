# secrest2-worker: SEGURIDAD (resto 2), lecturas y escrituras restantes de documentos trackeados

Rama `wt/secrest2`, base `wt/secrest-r` `beed8f22` (SEGURIDAD resto rebasada sobre main `02643fff`).
Contrato: TaskDoc
`task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views`
(task.debug). Files sumados por el coordinador: `selfdoc/python_materialize.py`, `selfdoc/materialize.py`,
`cli/selfdoc_inspect.py`, `cli/selfdoc_write.py` (decisión revisable: misma clase de lectura tras `.resolve()`).

## 1. Reproducción

La del coordinador (`coord2-ccconfig/secrest2/repro.log`, audit hook de `open`): con
`desk/tasks/task-repro-dos.md` symlink a `/dev/shm/outside-secret2/secreto-externo.md` y otra tarea que
lo enlaza con `[[task-repro-dos]]`, `sldb docs compose <otra> --render-links` abre el archivo de afuera
(`links/render.py:15`, `_title`) y emite `[task-repro-dos](../../../outside-secret2/secreto-externo.md)`.

## 2. Causa raíz

La guarda `sldb.store.source_read` (`unreadable_reason` + `read_source_text` con `O_NOFOLLOW`) existe,
pero cada lector decide si la usa. SEGURIDAD resto la puso en los seis comandos de su alcance; el resto
de las superficies arma la ruta del documento (`root / doc.path`, `runtime_doc["absolute_path"]`,
`node.semantics["path"]`, el destino de un enlace) y llama `read_text()`/`write_text()`, que siguen
symlinks. Tres agravantes:

1. **links/**: el resolver (`links/resolver.py:13,17-19,34-35`), `composer.compose_document` (:26) y
   `recovery.recover_links` (:24) hacen `.resolve()` del destino **antes** de cualquier chequeo: el
   symlink se pierde, el lector recibe la ruta de afuera y `render` la emite como href relativo.
2. **Escrituras**: `write_text` no usa `O_NOFOLLOW`. Donde hay `refuse_unreadable` previo
   (`payload_save_steps`, `replace_text`) queda la ventana TOCTOU entre el chequeo y la escritura;
   donde no lo hay (`create_document`, `backfill`, `builtin_relation_writes`, selfdoc) se escribe afuera.
3. **ELOOP**: `provenance_stamp.stamped_file` ya abre con `O_NOFOLLOW`; sus llamadores (`backfill`,
   `builtin_relation_writes`) propagan `OSError: [Errno 40]` en lugar de nombrar el hallazgo.
4. **selfdoc**: `_plan`/`_prepare` hacen `path.resolve()` de la salida en `knowledge/` y leen (y, si el
   documento no está trackeado, `_atomic_write` escribe) el destino del symlink.

## 3. Inventario (base beed8f22)

Criterio: ruta derivada de `doc.path`, `runtime_doc["absolute_path"]`, `node.semantics["path"]`, el
destino de un enlace resuelto, o la salida de selfdoc en `knowledge/` (documentos trackeados).
Piso: la lista del TaskDoc (`api/views/list_views.py:48` ya no existe en la base: H9 movió la lectura a
`api/views/view_source.py`, guardada). Lo marcado **(grep)** lo sumó el grep.

| archivo:línea | L/E | origen | superficie | tipo |
|---|---|---|---|---|
| api/model_registry/model_index_writes.py:63 | L | root / doc.path | models reindex (rehash) | agregada |
| api/edges/builtin_relation_writes.py:53 | L | path del doc | edges init relations | agregada |
| api/edges/builtin_relation_writes.py:28,55 | E | path del doc | edges init relations (stamped_file, ELOOP) | agregada |
| api/edges/rewrite_references.py:84 | L | project_root / path | edges rewrite | agregada |
| api/edges/project_graph/document_metadata.py:24 | L | path | project graph | agregada |
| api/edges/project_graph/project_texts.py:32 | L | root / relative_path | project graph | agregada |
| api/edges/project_graph/declared_target_nodes.py:63 | L | document | project graph | agregada |
| api/records/ast_target.py:38 | L | runtime_doc["absolute_path"] | records de un documento | objetivo único |
| api/records/fields.py:52 | L | project_root / doc.path | records | agregada |
| api/records/iter_records_docs.py:35,44 | L | doc_path | iter_records_docs | agregada |
| api/segments/build_document_segments.py:38 | L | store_path.parent / path | segments | agregada |
| cli/serve/document_routes.py:62 | L | runtime_doc["absolute_path"] | serve /document/ir | objetivo único |
| cli/serve/sections_routes.py:46 **(grep)** | L | root / runtime.path | serve sections | objetivo único |
| cli/commands/sections_show.py:27 | L | runtime_doc["absolute_path"] | sections show | objetivo único |
| cli/commands/sections_fields.py:44 **(grep)** | L | runtime_doc["absolute_path"] | sections fields | objetivo único |
| links/render.py:15 | L | destino resuelto | compose --render-links | enlace |
| links/recovery.py:14,28 | L | destino resuelto / doc | links | enlace |
| links/composer.py:10 **(grep)** | L | documento y destino de `![[x]]` | docs compose | enlace / objetivo único |
| links/resolver.py:13,17-19,34-35 **(grep)** | — | `.resolve()` previo | todos los enlaces | causa |
| models/structured_doc.py:87 | L | path | payload compuesto | objetivo único |
| api/model_drafts/backfill.py:66 **(grep)** | L | path del doc | models backfill | agregada |
| api/model_drafts/backfill.py:60 **(grep)** | E | path del doc | models backfill (stamped_file, ELOOP) | agregada |
| api/documents/create_document.py:51 **(grep)** | E | doc_path | docs create | objetivo único |
| api/documents/payload_save_steps.py:92 **(grep)** | E | root / doc_entry.path | docs update (TOCTOU) | objetivo único |
| api/documents/replace_text.py:78 + escritura | L/E | path | replace_text (TOCTOU, r3) | objetivo único |
| cli/commands/store_update.py | — | mensaje | stores update (r4) | mensaje |
| selfdoc/python_materialize.py:34 | L | output/symbols/<id>.md resuelto | selfdoc python | generado |
| selfdoc/materialize.py:41 | L | output/<kind>/<id>.md resuelto | selfdoc | generado |
| cli/selfdoc_inspect.py:68 | L | plan.path | selfdoc inspect (rename) | generado |
| cli/selfdoc_write.py:43 | L | plan.path | selfdoc write (before image) | generado |
| cli/selfdoc_write.py:61 | E | plan.path | selfdoc write (no trackeado) | generado |

Excepciones del grep (no son documentos trackeados): `api/model_drafts/{source_location,template_literals,
field_blocks,metadata_literals,field_drafts,metadata_drafts,metadata_composition_sync,template_drafts,
draft_restore,draft_validation}` (fuentes Python de modelos); `cli/commands/{init,faq,graph,lint,
models_create,models_validate,models_metadata,predicates_file,doc,explore_code,explore_docs,inbox_parse}`
(archivo que nombra el usuario, assets del paquete o docs/ del repo); `cli/commands/inbox_create.py:36,96`
(la nota nueva que el comando crea y valida antes de trackear; el track pasa por `track_document`);
`api/documents/transaction_ops.py:71,76` (`write_file` plano, excepción de SEGURIDAD resto);
`selfdoc/python_materialize.py:58` (spec de arquitectura, chequeada dentro de la raíz),
`selfdoc/python_scanner.py`, `python_source_scan.py`, `source_graph_file.py` (fuentes Python y json);
y las de SEGURIDAD resto en store/ (yaml, caches, pyproject, .gitignore, rollback, lock).

## 4. Arreglo (r1-r6)

**Un helper, una forma por superficie** (`src/sldb/store/source_guard.py`, archivo nuevo en el eje
`lectura_de_fuentes`, sumado a sus `paths`). Usa `source_read` (`unreadable_reason`,
`read_source_text`) y toma `SLDBDocumentTargetError` de la costura `store/exceptions.py` (que ahora lo
reexporta; `tests/test_store_seams.py`). Usa también los códigos de `stores check` (`READ_CODES`: `store/path-outside-root`,
`store/symlink-not-read`; viven acá porque store/ y links/ no importan api/):

- `unread_line(root, path, subject)` → `[code] subject: why; sldb does not read it` (nunca la ruta de destino).
- `target_text` / `refuse_unread` (objetivo único) → `SLDBDocumentTargetError`, exit 1 (`docs/missing`).
- `aggregate_text` (agregadas) → warning por logging (`[warning]` en la CLI) y `None`.
- `write_source_text` / `write_source_bytes` / `read_source_bytes` → `O_NOFOLLOW`; ELOOP se nombra
  como `store/symlink-not-read`. `target_write` = chequeo + escritura.

| archivo:línea (antes, beed8f22) | L/E | antes | después |
|---|---|---|---|
| api/model_registry/model_index_writes.py:63 | L | `read_text` | `aggregate_text` (:65), warning y el doc conserva sus hashes |
| api/edges/builtin_relation_writes.py:28 | E | `write_text(stamped_file(...))`, ELOOP | `_write_builtin`: `unread_line` + warning (:39-43), `write_source_text` |
| api/edges/builtin_relation_writes.py:53,55 | L/E | `read_text` / `write_text` | `aggregate_text` (:65), `write_source_text` (:69) |
| api/edges/rewrite_references.py:84 | L | `read_text` | `aggregate_text` (:85): no leído = skip con razón; el reescritor de líneas pasó a `rewrite_mentions.rewritten_text` (límite de 80 líneas) |
| api/edges/project_graph/document_metadata.py:24 | L | `read_text` | `aggregate_text` (:28), parámetro nuevo opcional `root` (document_nodes.py lo pasa) |
| api/edges/project_graph/project_texts.py:32 | L | `read_text` | `aggregate_text` (:33), texto vacío |
| api/edges/project_graph/declared_target_nodes.py:63 | L | `read_text` | `aggregate_text` (:64) |
| api/records/ast_target.py:38 | L | `read_text` de `absolute_path` | `runtime_document` rechaza antes con el código (document_payload.py:33,48); `read_source_text` (:39) |
| api/records/fields.py:52 | L | `read_text` | `aggregate_text` (:52) |
| api/records/iter_records_docs.py:35,44 | L | dos `read_text` | una `aggregate_text` (:37), el texto pasa a `_add_rebuilt_sections` |
| api/segments/build_document_segments.py:38 | L | `read_text` | `target_text` (:41) |
| api/views/view_source.py (H9, ya guardada) | L | `unreadable_reason` + mensaje sin código | `target_text` (:58) con código; `readable_view_node` (:65) para `list_views`, que avisa y sigue |
| api/documents/document_payload.py:31 | — | `Unknown document target` para un doc no leído | `_refuse_unread` (:48) nombra el código |
| api/documents/create_document.py:51 | E | `write_text` tras `.resolve()` | `_resolve_path` rechaza un symlink antes de resolver (:71); `write_source_text` (:53) |
| api/documents/payload_save_steps.py:92 | E | `write_text` tras `refuse_unreadable` | `write_source_text` (:93) |
| api/documents/provenance_stamp.py:32 | L | `read_source_text` (ELOOP crudo) | `read_source_bytes` (:33): `store/symlink-not-read` |
| api/documents/replace_text.py:78 | L | `read_bytes` | `read_source_bytes` (:79) |
| api/documents/transaction_ops.py:71,76 | L/E | `read_bytes` / `write_bytes` | `read_source_bytes` (:72), `write_source_bytes` (:77) |
| api/model_drafts/backfill.py:60,66 | L/E | `write_text(stamped_file)` / `read_text` | `aggregate_text` (:67), `write_source_text` (:61) |
| cli/serve/document_routes.py:62 | L | `read_text` | `read_source_text` (:63) tras `runtime_document` con código |
| cli/serve/sections_routes.py:46 | L | `read_text` | `target_text` (:47) |
| cli/commands/sections_show.py:27 | L | `read_text` | `read_source_text` (:28) tras `runtime_document` |
| cli/commands/sections_fields.py:44 | L | `read_text` | `read_source_text` (:45) tras `runtime_document` |
| cli/commands/store_update.py:29 | — | todo bajo `Skipped missing documents` | `Skipped unread documents: b (store/...)` aparte |
| links/resolver.py:13,17-19,34-35 | — | `.resolve()` antes de chequear | `_tracked_documents` filtra por `unreadable_reason` (:24), `resolve_document_input` → `_refuse` (:35), `_readable` antes de resolver (:32) |
| links/render.py:15 | L | `read_text` | `read_source_text` (:16), destino ya filtrado |
| links/recovery.py:14,28 | L | `read_text` | `read_source_text` (:15, :29) |
| links/composer.py:10 | L | `read_text` | `read_source_text` (:11) |
| models/structured_doc.py:87 | L | `read_text` | guarda inline (:69: symlink o fuera de `ref_root` → None) + `O_NOFOLLOW` (:89) |
| selfdoc/python_materialize.py:34 | L | `read_text` tras `.resolve()` | `refuse_unread` antes de resolver (:35), `read_source_text` (:37) |
| selfdoc/materialize.py:41 | L | ídem | `refuse_unread` (:42), `read_source_text` (:44) |
| cli/selfdoc_inspect.py:68 | L | `read_text` | `target_text` (:70) |
| cli/selfdoc_write.py:43 | L | `read_text` | `read_source_text` (:44) sobre el path ya chequeado por el plan |

## 5. Grep final

`grep -rnE "\.read_text\(|\.read_bytes\(|[^_.a-z]open\(|os\.open\(|\.write_text\(|\.write_bytes\("`
sobre las superficies de la tabla (y `store/source_guard.py`):

```
src/sldb/selfdoc/python_materialize.py:61   spec de arquitectura, chequeada dentro de la raíz (no es documento trackeado)
src/sldb/models/structured_doc.py:89        os.open con O_NOFOLLOW tras la guarda inline (capa 0)
src/sldb/store/source_guard.py:74,80,86     el punto de apertura con O_NOFOLLOW
```

El resto de `src/sldb` queda en las excepciones de §3 (fuentes Python de modelos, archivos que nombra
el usuario, yaml/caches/lock del store, `transaction_ops` ahora con `O_NOFOLLOW`).
`cli/selfdoc_write.py:61` (`StoreIOUtils._atomic_write`, documento no trackeado) escribe un temporal y
hace `os.replace`, que reemplaza un symlink en lugar de seguirlo; el path ya pasó por `refuse_unread`.

## 6. Tests

Nuevos, un archivo por superficie en `tests/security/` (helper `audited.py`: CLI o API en un proceso
nuevo con audit hook de `open`; el secreto no se abre ni con un intento `O_NOFOLLOW`, porque el
evento sale antes del syscall):

| archivo | casos | en la base beed8f22 |
|---|---|---|
| test_guard_links.py | render-links, transclusión, compose del symlink, links | 3 de 4 fallan |
| test_guard_edges.py | rebuild, project graph (referrers), rewrite | 2 de 3 fallan (rebuild ya guardado por secrest) |
| test_guard_edges_init.py | builtin relation sobre symlink | falla (ELOOP) |
| test_guard_records.py | ast show docs/b, find --rebuild, field records | 1 de 3 falla |
| test_guard_views.py | list_views sigue, run_view con código | 2 fallan |
| test_guard_serve.py | /document/ir b, /document/ir a, sections ir | 2 de 3 fallan |
| test_guard_segments.py | b, a, canonical con swap | 2 de 3 fallan |
| test_guard_sections_show.py | sections show b, sections fields docs/b/status, show a | 2 de 3 fallan |
| test_guard_model_registry.py | reindex_model | falla |
| test_guard_selfdoc.py | python-sync con symlink en knowledge/symbols | falla |
| test_replace_text_race.py | swap tras el chequeo; swap tras la lectura | 1 de 2 falla (el segundo ya lo frena `transaction_paths.inside`) |
| test_store_update_message.py | unread vs missing; symlink interno | 2 fallan |

Todos en verde en la rama. Regresión, de a uno con la guarda de pgrep: los 151 archivos de `tests/`
que el grep cruza con las funciones cambiadas (`create_document`, `runtime_document`, compose, sections,
serve, segments, records, referrers/rewrite, project graph, relation types, reindex, backfill,
replace_text, transaction, payload save, stores update, selfdoc, views, composition) más los 12 nuevos
y `test_clean_code_rules.py` (959 passed): 163 archivos. Primera pasada: 162 en verde y
`tests/test_store_seams.py` con 1 fallo (`source_guard.py` importaba `sldb.core.exceptions`; el store
solo importa el núcleo por `store/exceptions.py`). Corregido: `store/exceptions.py` reexporta
`SLDBDocumentTargetError` y `source_guard` lo toma de ahí; `test_store_seams.py` y
`test_guard_segments.py` vueltos a correr en verde. Saltados por entorno, como en main (tree-sitter
no instalado, extra `[code]`): `test_anchors.py`, `test_machine_editor_schema.py`,
`test_fingerprints.py`, `test_treesitter_agreement.py`, `test_treesitter_symbols.py`.
`test_live_stale_security.py` y `test_tracked_reads_guarded.py` en verde.

`tests/test_clean_code_rules.py` en verde sin subir límites (se partieron
`write_builtin_relation_types` → `_write_builtin` y `_planned_text` → `rewrite_mentions.rewritten_text`).
`bash tools/check.sh --fast`: PASS. Grados medidos (`contracts/layers.toml`, comentarios del
2026-11-11): nucleo needed_by 50→54, adaptadores needs 5→6, operacion needs 70→71, enlaces needs 2→4.

## 7. Decisiones revisables

1. **Códigos en store/**: `READ_CODES` duplica en `source_guard` los dos valores de
   `store_findings._DOC_CODES` (api/), porque store/ y links/ no importan api/.
2. **`runtime_document` nombra el hallazgo**: un nombre que es un documento no leído da
   `SLDBDocumentTargetError('[store/path-outside-root] ...')` en lugar de `Unknown document target`
   (exit 1 en ambos casos). Así todos los objetivos únicos que pasan por él (sections, ast, serve,
   segments, docs update) dan el código sin leer.
3. **Lectores de `absolute_path`** (sections show/fields, ast, serve /document/ir): el documento ya
   pasó la guarda al cargarse; leen la ruta resuelta con `O_NOFOLLOW` sin cambiar la forma del dict.
4. **links sin store**: la raíz de la guarda es la carpeta del propio archivo (solo se rechaza el
   symlink del último componente); con store, la raíz del proyecto. Un destino rechazado no avisa:
   queda sin resolver, como un enlace roto.
5. **`models/structured_doc.py`** repite la guarda inline (3 líneas) en vez de importar store/: la
   arista models→store ya es la excepción R6 y no se agranda.
6. **`create_document`** rechaza un path que es symlink, pero sigue creando un path plano fuera del
   proyecto (decisión 2 de SEGURIDAD resto, spec2viz).
7. **Rewrite**: una mención en un archivo no leído va a `skipped` con la razón; los demás se reescriben.
8. **Base movida**: el inventario se hizo sobre ca578fd2 y se reconfirmó sobre beed8f22;
   `api/views/list_views.py:48` ya no existía (H9), pero `list_views` abortaba ante una vista no
   legible y ahora avisa y sigue.

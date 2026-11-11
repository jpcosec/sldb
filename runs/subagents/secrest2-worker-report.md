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

## 4. Arreglo

_(sigue en el commit del arreglo)_

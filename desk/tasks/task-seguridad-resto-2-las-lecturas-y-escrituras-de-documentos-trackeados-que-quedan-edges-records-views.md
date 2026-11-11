---
sldb:
  by: agent
  at: '2026-11-11T18:03:11Z'
  authority: generated
  via: save_document_payload
id: task-seguridad-resto-2-las-lecturas-y-escrituras-de-documentos-trackeados-que-quedan-edges-records-views
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/model_registry/
- src/sldb/api/edges/
- src/sldb/api/views/
- src/sldb/api/records/
- src/sldb/api/segments/
- src/sldb/api/model_drafts/
- src/sldb/api/documents/
- src/sldb/cli/serve/
- src/sldb/cli/commands/
- src/sldb/links/
- src/sldb/models/structured_doc.py
- src/sldb/store/
- src/sldb/selfdoc/python_materialize.py
- src/sldb/selfdoc/materialize.py
- src/sldb/cli/selfdoc_inspect.py
- src/sldb/cli/selfdoc_write.py
- tests/
- docs/
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-seguridad-resto-2-lecturas-de-documentos-trackeados-sin-la-guarda-fuera-de-los-seis-comandos-toctou-de-replace-text-y-el-mensaje-de-stores-update.md
---

# SEGURIDAD (resto 2): las lecturas y escrituras de documentos trackeados que quedan (edges, records, views, serve, links, segments, sections show, model_registry, structured_doc) pasan por la guarda de raíz y symlinks; TOCTOU de replace_text y mensaje de stores update

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord, continuación de SEGURIDAD resto (wt/secrest ca578fd2), que cubrió stores check/update/build/build --check y docs track/update y cerró un hallazgo grave: docs update de un documento trackeado symlink escribía el archivo de afuera. Su §7 lista 17 lecturas sin guarda fuera de sus files; reproducido: docs compose --render-links abre un documento trackeado symlink fuera de la raíz.

## Goal

_Describe the concrete result this task must produce._

Ningún comando ni función de la API lee o escribe el texto de un documento trackeado que sea symlink o resuelva fuera de la raíz: toda lectura pasa por sldb.store.source_read y toda escritura abre con O_NOFOLLOW, con un test de audit hook por superficie y el grep final vacío o con excepciones nombradas.

## Scope

_State what is in scope and what is out of scope._

En alcance: las lecturas listadas en implementation_path, los llamadores de provenance_stamp.stamped_file (model_drafts/backfill.py, edges/builtin_relation_writes.py), el TOCTOU de api/documents/replace_text.py y el mensaje de cli/commands/store_update.py. Fuera: lo que ya cubrió SEGURIDAD resto (stores check/update/build, docs track/update), el comportamiento de stale/rebuild y la forma de los hallazgos existentes (store/path-outside-root, store/symlink-not-read).

## Implementation Path

_Outline the expected implementation route or affected surface._

BASE: sldb main con wt/secrest integrada (ca578fd2). sldb.store.source_read (unreadable_reason + read_source_text con O_NOFOLLOW, eje lectura_de_fuentes) es el único punto de apertura; load_runtime_documents ya no devuelve un documento no leído, pero varias superficies leen por su cuenta.

REPRODUCCIÓN (coordinador, sobre ca578fd2; runs/subagents/20261111-repro-secrest2/repro.log con audit_run.py, audit hook de 'open'): con la tarea trackeada task-repro-dos como symlink a /dev/shm/outside-secret2/secreto-externo.md y otra tarea que lo enlaza con [[task-repro-dos]], 'sldb docs compose <otra> --render-links' abre el archivo de afuera (links/render.py:15 _title) y emite un enlace relativo hacia fuera de la raíz.

CAUSA (lecturas por root / doc.path o ruta resuelta sin la guarda; inventario del informe de SEGURIDAD resto §7, a confirmar y completar por grep): api/model_registry/model_index_writes.py:63, api/edges/builtin_relation_writes.py:53, api/edges/rewrite_references.py:84, api/edges/project_graph/document_metadata.py:24, api/edges/project_graph/project_texts.py:32, api/edges/project_graph/declared_target_nodes.py:63, api/views/list_views.py:48, api/records/ast_target.py:38, api/records/fields.py:52, api/records/iter_records_docs.py:35,44, api/segments/build_document_segments.py:38, cli/serve/document_routes.py:62, cli/commands/sections_show.py:27, links/render.py:15, links/recovery.py:14,28, models/structured_doc.py:87. provenance_stamp.stamped_file ahora abre con O_NOFOLLOW: sus llamadores (model_drafts/backfill.py, edges/builtin_relation_writes.py) fallan con ELOOP ante un symlink en vez de nombrar el hallazgo.

ARREGLO (r1-r6):
r1 (lecturas): cada lectura de la lista pasa por source_read (unreadable_reason y después read_source_text). Un documento fuera de la raíz o symlink no se lee: la superficie lo nombra con el hallazgo existente y sigue con los demás, o falla con error claro cuando el documento es el objetivo único del comando. Un enlace (links/render, links/recovery) cuyo destino resuelve fuera de la raíz o es symlink no se abre ni se emite como enlace.
r2 (escrituras y ELOOP): los llamadores de stamped_file y toda escritura de un documento trackeado de esta lista capturan el caso symlink y lo nombran con el hallazgo en lugar de propagar ELOOP u OSError.
r3 (TOCTOU de replace_text): el read_bytes y la escritura de api/documents/replace_text.py abren con O_NOFOLLOW (o por source_read), de modo que una carrera que cambie el archivo por un symlink entre el chequeo y la escritura falla sin escribir afuera. Test que simula la carrera (por ejemplo, monkeypatch entre chequeo y escritura).
r4 (mensaje de stores update): cli/commands/store_update.py deja de listar bajo 'Skipped missing documents' un documento no leído por la guarda; lo nombra con su código (store/path-outside-root o store/symlink-not-read).
r5 (inventario y tests): el informe trae la tabla de cada lectura y escritura tocada (archivo:línea, antes y después) y el grep final de read_text/read_bytes/open sobre rutas de documentos trackeados fuera de source_read, vacío o con cada excepción justificada. Tests de regresión con audit hook de 'open' en subproceso, uno por superficie: edges (rebuild/rewrite/project graph), records, views, serve (/document/ir), links (compose --render-links), segments, sections show, model_registry. Los tests de seguridad existentes (test_live_stale_security.py, test_tracked_reads_guarded.py) siguen verdes.
r6 (límites): tests/test_clean_code_rules.py OBLIGATORIO (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites). Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml. Los grados medidos de unidad se actualizan con comentario fechado si cambian.

VALIDACIÓN: el worker corre los tests que toca, todos los que pasan por las funciones cambiadas (grep), test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Tests con audit hook en subproceso por superficie (edges, records, views, serve, links, segments, sections show, model_registry): ninguna abre el symlink saliente y nombran el hallazgo
- replace_text: la carrera symlink entre chequeo y escritura no escribe afuera
- stores update nombra store/path-outside-root o store/symlink-not-read en lugar de Skipped missing
- test_live_stale_security, test_tracked_reads_guarded y los tests tocados en verde
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r6 hechos con causa raíz escrita, inventario y grep final en el informe, tests verdes; CHANGELOG y docs actualizados.

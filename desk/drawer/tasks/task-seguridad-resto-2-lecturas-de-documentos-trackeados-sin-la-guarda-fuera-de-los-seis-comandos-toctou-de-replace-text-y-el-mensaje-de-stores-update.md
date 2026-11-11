---
id: task-seguridad-resto-2-lecturas-de-documentos-trackeados-sin-la-guarda-fuera-de-los-seis-comandos-toctou-de-replace-text-y-el-mensaje-de-stores-update
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SEGURIDAD (resto 2): lecturas de documentos trackeados sin la guarda fuera de los seis comandos, TOCTOU de replace_text y el mensaje de stores update

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-seguridad-resto-2-lecturas-de-documentos-trackeados-sin-la-guarda-fuera-de-los-seis-comandos-toctou.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-seguridad-resto-2-lecturas-de-documentos-trackeados-sin-la-guarda-fuera-de-los-seis-comandos-toctou.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Lo deja la tarea SEGURIDAD resto (wt/secrest ca578fd2, runs/subagents/secrest-worker-report.md §7 y §8). Esa tarea cubrió stores check/update/build/build --check y docs track/update, y cerró un hallazgo grave: en main, docs update sobre un documento trackeado que es symlink ESCRIBÍA el archivo de afuera. Quedan, fuera de sus files:
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
Además (§8): (3) cli/commands/store_update.py lista bajo 'Skipped missing documents' un documento no leído por la guarda; el mensaje debe nombrar el código (store/path-outside-root o store/symlink-not-read). (4) TOCTOU: la escritura y el read_bytes de replace_text siguen sin O_NOFOLLOW tras el chequeo; una carrera que cambie el archivo por un symlink entre chequeo y escritura no está cubierta.
Hecho cuando cada lectura y escritura de un documento trackeado de esa lista pase por sldb.store.source_read (o una escritura equivalente con O_NOFOLLOW), con tests de audit hook por superficie (edges, records, views, serve, links, segments, sections_show), y el grep final quede vacío o con excepciones nombradas.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

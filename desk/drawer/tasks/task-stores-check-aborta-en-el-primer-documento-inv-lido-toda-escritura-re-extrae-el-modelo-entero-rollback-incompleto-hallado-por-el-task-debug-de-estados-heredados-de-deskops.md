---
id: task-stores-check-aborta-en-el-primer-documento-inv-lido-toda-escritura-re-extrae-el-modelo-entero-rollback-incompleto-hallado-por-el-task-debug-de-estados-heredados-de-deskops
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

# stores check aborta en el primer documento inválido; toda escritura re-extrae el modelo entero; rollback incompleto (hallado por el task.debug de estados heredados de deskops)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-stores-check-aborta-en-el-primer-documento-inválido-toda-escritura-re-extrae-el-modelo-entero-rollba.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-stores-check-aborta-en-el-primer-documento-inválido-toda-escritura-re-extrae-el-modelo-entero-rollba.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por el worker del task.debug de estados heredados de deskops (wt/legacy-status 545a2fda, runs/subagents/legacy-worker-report.md), sobre una copia de /srv/repos/shared_llm-gateway con sldb 84eb7f75. Un desk con un documento que su modelo rechaza (tareas pre-CC31 con status terminal y history vacía) deja de poder diagnosticarse y escribirse.

## Hipótesis para sldb (b5: las abre el coordinador; el worker no escribe en sldb)

Todas verificadas sobre una copia del gateway en `/dev/shm` con sldb `84eb7f75`.

- **H1 (stores check aborta en el primer documento inválido).** `sldb.store.diagnostics.diagnose_store` →
  `_diagnose_model` → `_diagnose_doc` → `_fields_state` → `hashing.hash_fields_with_map` → `extract_model_data`
  no tiene guarda por documento: el `ValidationError` de un documento sale de `check_store` y `sldb.cli.main`
  imprime `Unexpected: ...`, rc 1, sin JSON. Lo esperable es un hallazgo por documento (nota `invalid` o similar)
  y el resto del diagnóstico. deskops lo esquiva leyendo las tareas por frontmatter.
- **H2 (toda escritura del store re-extrae todos los documentos del modelo).** `sldb.api.replace_text` dentro de
  `transaction`: el `untrack` del documento llama `untrack_document._forget` → `forget_document` →
  `edge_rebuild.rebuild_edges_indexes` → `edge_sync._sync_model_docs`, que extrae con el modelo cada documento del
  modelo y cae en cualquier otro inválido. Lo mismo `add_model`/herencia de modelos (`init_local_store`: "Inheriting
  ReviewDoc ... Error: 1 validation error for TaskDoc") y `closeout retire` (untrack de la tarea). Consecuencia: con
  dos tareas inválidas trackeadas en el mismo modelo no se puede escribir ninguna por la vía de documentos de b8.
- **H3 (rollback incompleto).** En el caso de H2 la transacción termina en
  `RollbackError: Rollback incomplete; not restored: .sldb/core/documents/TaskDoc/<...>.yaml, ...` y deja esos
  índices modificados en el árbol (visto en `git status` de la copia). Una transacción fallida no debería dejar el
  store a medio escribir.

Esperado: H1, un hallazgo por documento inválido y el resto del diagnóstico; H2, una escritura de un documento no re-valida todos los del modelo, o al menos no cae por otro documento; H3, el rollback de una transacción fallida restaura todo lo que escribió.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

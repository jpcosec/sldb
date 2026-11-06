---
id: task-on-write-no-se-eval-a-en-create-document-ni-en-track-document-file
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

# on_write no se evalúa en create_document ni en track_document_file

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-on-write-no-se-evalúa-en-create-document-ni-en-track-document-file.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-on-write-no-se-evalúa-en-create-document-ni-en-track-document-file.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallazgo de GD27 (plan generalizar-desde-deskops, 2026-11-06), seguimiento de GO08.

**Qué pasa.** `check_on_write` de GO08 (src/sldb/api/rules/rules_on_write.py) solo se llama desde `save_document_payload` (src/sldb/api/documents/payload_save.py:47, vía `check_rules_on_write` de payload_save_steps.py). `create_document` (api/documents/create_document.py) y `track_document_file` (api/documents/track_document_file.py) no evalúan las reglas `on_write`: un documento nuevo, o uno que se empieza a trackear, entra al store sin pasar por las RuleDocs `on_write` de usuario ni por la familia incorporada `builtin:tag_namespace` (GD27). Solo lo detectan después `on_check` (stores check), `sldb rules check` y `sldb tags check`.

**Cambio de comportamiento si se extiende.** Hacer que create y track evalúen `on_write` cambia lo que hoy hacen las RuleDocs de usuario:
- un `create_document` o `docs create` o `docs track` que hoy pasa podría empezar a fallar con `SLDBRuleViolationError` si viola una regla `on_write` existente;
- `apply_batch`, `/save` con create y track, `transaction.create` y `transaction.track` (GD24), y `scaffold_store` (GD26, seeds document con track) heredarían el rechazo;
- `stores build` (apply_includes) trackea en lote: una regla `on_write` podría frenar un build que hoy pasa (habría que decidir si build evalúa o no).

**Decisión del dueño.** Extender `on_write` a create y track es decisión del dueño: es un cambio de contrato de las reglas de usuario (rules.md §9), no un arreglo local. Mientras no se decida, GD27 (q18) prueba el rechazo por save, `transaction.update` y `replace_text`, y deja create y track cubiertos por `on_check` y `tags check`.

**Evidencia.** TaskDoc de GD27, precisión q18 (sldb 7ff04fd0); grep de `check_rules_on_write` y `check_on_write` en src/sldb/api/documents/.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

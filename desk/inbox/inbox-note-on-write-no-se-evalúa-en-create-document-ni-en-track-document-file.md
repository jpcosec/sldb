---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-06T22:26:33Z'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# on_write no se evalúa en create_document ni en track_document_file

_Describe the incoming message with enough evidence to triage._

Hallazgo de GD27 (plan generalizar-desde-deskops, 2026-11-06), seguimiento de GO08.

**Qué pasa.** `check_on_write` de GO08 (src/sldb/api/rules/rules_on_write.py) solo se llama desde `save_document_payload` (src/sldb/api/documents/payload_save.py:47, vía `check_rules_on_write` de payload_save_steps.py). `create_document` (api/documents/create_document.py) y `track_document_file` (api/documents/track_document_file.py) no evalúan las reglas `on_write`: un documento nuevo, o uno que se empieza a trackear, entra al store sin pasar por las RuleDocs `on_write` de usuario ni por la familia incorporada `builtin:tag_namespace` (GD27). Solo lo detectan después `on_check` (stores check), `sldb rules check` y `sldb tags check`.

**Cambio de comportamiento si se extiende.** Hacer que create y track evalúen `on_write` cambia lo que hoy hacen las RuleDocs de usuario:
- un `create_document` o `docs create` o `docs track` que hoy pasa podría empezar a fallar con `SLDBRuleViolationError` si viola una regla `on_write` existente;
- `apply_batch`, `/save` con create y track, `transaction.create` y `transaction.track` (GD24), y `scaffold_store` (GD26, seeds document con track) heredarían el rechazo;
- `stores build` (apply_includes) trackea en lote: una regla `on_write` podría frenar un build que hoy pasa (habría que decidir si build evalúa o no).

**Decisión del dueño.** Extender `on_write` a create y track es decisión del dueño: es un cambio de contrato de las reglas de usuario (rules.md §9), no un arreglo local. Mientras no se decida, GD27 (q18) prueba el rechazo por save, `transaction.update` y `replace_text`, y deja create y track cubiertos por `on_check` y `tags check`.

**Evidencia.** TaskDoc de GD27, precisión q18 (sldb 7ff04fd0); grep de `check_rules_on_write` y `check_on_write` en src/sldb/api/documents/.

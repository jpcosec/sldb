---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-26T01:01:02'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb fields remove exige un argumento value y no lo usa

_Describe the incoming message with enough evidence to triage._

Hallazgo de la revisión del modelo (2026-11-25). El parser de `sldb fields remove` pide un argumento posicional `value` y el comando lo ignora (src/sldb/cli/commands/fields_mutate.py). Quien llama tiene que inventar un valor para borrar un campo. Pedido: quitar el argumento, o decir para qué es.

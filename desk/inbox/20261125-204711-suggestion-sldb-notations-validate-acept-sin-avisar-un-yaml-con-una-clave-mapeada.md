---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T20:47:11'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb notations validate aceptó sin avisar un YAML con una clave mapeada 

_Describe the incoming message with enough evidence to triage._

sldb notations validate aceptó sin avisar un YAML con una clave mapeada duplicada (data: dos veces en el mismo mapa) en specs/negocio/estados-revision.yml de MEPU (25-11, DOC-15; el error ya se corrigió en el spec). YAML con claves duplicadas debería fallar la validación (o al menos advertir), porque el loader se queda con la última y se pierde la primera en silencio.

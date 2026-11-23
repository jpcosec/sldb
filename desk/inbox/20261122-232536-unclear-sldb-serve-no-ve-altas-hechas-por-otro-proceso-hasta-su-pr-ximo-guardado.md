---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T23:25:36'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# sldb serve no ve altas hechas por otro proceso hasta su próximo guardado

_Describe the incoming message with enough evidence to triage._

sldb serve no ve lo que otro proceso escribe en el store (create_document desde la API de Python) hasta su propio próximo guardado: /graph y /document/segments siguen sin el documento nuevo (404 Unknown doc). Reproducido en minegocio el 2026-11-22: serve arriba, Almacen.crear por fuera, GET /graph no lo lista; tras un POST /save cualquiera aparece. Afecta a un store que edita un agente por CLI mientras la superficie está abierta.

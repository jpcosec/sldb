---
sldb:
  by: agent
  at: '2026-11-23T17:57:38Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-22T23:25:36'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:57:04'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-sldb-serve-tolera-documentos-invalidos-ve-altas-de-otros-procesos-y-resuelve-tipo-nombre-en-document
  (sesion de minegocio, triaje 2026-11-23); el lector de surface la referencia cuando
  toca su pantalla
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb serve no ve altas hechas por otro proceso hasta su próximo guardado

_Describe the incoming message with enough evidence to triage._

sldb serve no ve lo que otro proceso escribe en el store (create_document desde la API de Python) hasta su propio próximo guardado: /graph y /document/segments siguen sin el documento nuevo (404 Unknown doc). Reproducido en minegocio el 2026-11-22: serve arriba, Almacen.crear por fuera, GET /graph no lo lista; tras un POST /save cualquiera aparece. Afecta a un store que edita un agente por CLI mientras la superficie está abierta.

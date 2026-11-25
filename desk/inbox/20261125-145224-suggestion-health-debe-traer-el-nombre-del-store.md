---
sldb:
  by: agent
  at: '2026-11-25T15:33:53Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T14:52:24'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T12:33:22'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'incorrecta: GET /stores ya expone la ruta del store (stores_routes.py:33-35);
  el intento 2 de la tarea del alias la usa'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# /health debe traer el nombre del store

_Describe the incoming message with enough evidence to triage._

surface muestra en Lectura el nombre del store servido (WorkbenchShell prop storePath, via storeTitle) pero sldb serve no lo expone: /health y /schema no traen ruta ni nombre. Pedimos agregar store_path o store_name a /health. Mientras, Lectura muestra 'Documentos'.

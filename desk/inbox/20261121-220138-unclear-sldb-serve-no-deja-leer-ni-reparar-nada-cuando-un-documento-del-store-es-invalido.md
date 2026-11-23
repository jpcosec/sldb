---
sldb:
  by: agent
  at: '2026-11-23T17:56:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T22:01:38'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:56:26'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-sldb-serve-tolera-documentos-invalidos-ve-altas-de-otros-procesos-y-resuelve-tipo-nombre-en-document
  (sesion de minegocio, triaje 2026-11-23); el lector de surface la referencia cuando
  toca su pantalla
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb serve no deja leer ni reparar nada cuando un documento del store es invalido

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21): con un documento del store fuera de contrato al arrancar 'sldb serve' (un servicio con duracion_min: 2 en negocios/<n>/wiki), GET /graph responde 500, GET /document/segments de OTRO documento sano responde 422 y POST /save sobre ese documento sano responde 500 (cli/serve/save_routes.py:33-42). Esperado: como load_runtime_documents(on_invalid='skip') en la API de Python, el servidor entrega los documentos sanos, nombra aparte los rechazados y deja abrir y reparar el rechazado. Real: una sola pagina rota deja la superficie sin poder leer ni reparar nada; hay que arreglarla por CLI o a mano. Pedido: lectura tolerante en /graph, /document y /document/segments con la lista de rechazados, y que /save pueda escribir sobre un documento rechazado para repararlo.

---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T22:01:38'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# sldb serve no deja leer ni reparar nada cuando un documento del store es invalido

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21): con un documento del store fuera de contrato al arrancar 'sldb serve' (un servicio con duracion_min: 2 en negocios/<n>/wiki), GET /graph responde 500, GET /document/segments de OTRO documento sano responde 422 y POST /save sobre ese documento sano responde 500 (cli/serve/save_routes.py:33-42). Esperado: como load_runtime_documents(on_invalid='skip') en la API de Python, el servidor entrega los documentos sanos, nombra aparte los rechazados y deja abrir y reparar el rechazado. Real: una sola pagina rota deja la superficie sin poder leer ni reparar nada; hay que arreglarla por CLI o a mano. Pedido: lectura tolerante en /graph, /document y /document/segments con la lista de rechazados, y que /save pueda escribir sobre un documento rechazado para repararlo.

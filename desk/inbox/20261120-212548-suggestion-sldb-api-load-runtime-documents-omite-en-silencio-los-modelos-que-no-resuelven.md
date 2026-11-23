---
sldb:
  by: agent
  at: '2026-11-23T01:42:48Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-20T21:25:48'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T22:42:24'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en la tarea task-load-runtime-documents-informa-los-modelos-que-no-pudo-resolver-en-vez-de-omitirlos-en-silencio.
  Sigue en 6ab01b80: _resolve_model_type traga la excepción y _load_one hace continue.
  Está relacionada con task-docs-show-sobre-un-store-enlazado-dice-que-no-pudo-importar-el-modelo-en-vez-de-unknown-document-tar.'
---

# sldb.api.load_runtime_documents omite en silencio los modelos que no resuelven

_Describe the incoming message with enough evidence to triage._

2026-11-20, IR (tarea de cierre de IR04b): load_runtime_documents recorre los modelos del store_index y salta sin aviso los que _resolve_model_type no resuelve. En el store de prueba de IR, los modelos heredados de deskops (model_ref deskops.models...) no resuelven hasta que algo los importa, así que la misma llamada devuelve 53 documentos al principio y 506 después de una escritura en el mismo proceso. Pedido: que avise (warning o campo en el resultado) de los modelos que no pudo resolver, o que acepte un pythonpath para resolverlos, en vez de omitirlos sin decir nada.

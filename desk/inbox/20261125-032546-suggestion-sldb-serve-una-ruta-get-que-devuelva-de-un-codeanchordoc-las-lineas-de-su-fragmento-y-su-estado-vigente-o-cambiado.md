---
sldb:
  by: agent
  at: '2026-11-25T06:29:33Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T03:25:46'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T03:29:08'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en tarea de sldb
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb serve: una ruta GET que devuelva de un CodeAnchorDoc las lineas de su fragmento y su estado vigente o cambiado

_Describe the incoming message with enough evidence to triage._

Pedido de IR (U9, pestana Anclajes de la UI de specIR). sldb serve no lee codigo ni anclas: /document de un CodeAnchorDoc da metadatos, pero no el texto del fragmento ni si sigue vigente. Ambas cosas son de sldb (sldb.api.anchors.check_anchors). Pedido: GET que, para un anchor, devuelva ruta, rango de lineas, las lineas del fragmento (con algo de contexto) y el estado (intact/changed/lost) que calcula sldb. Solo lectura. Respuesta esperada: tarea en sldb o nota de vuelta a IR.

---
sldb:
  by: agent
  at: '2026-11-25T21:51:33Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T21:30:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T18:51:07'
# why the note was acknowledged; empty when no reason was given
ack_reason: Tarea task-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by-y-la-vista-resuelta-lo-pasa-tal-cual
# conversation thread/message the note came from, e.g. #hilo/1234
---

# LAYOUT_KINDS: aceptar partition-lanes con by

_Describe the incoming message with enough evidence to triage._

graph_ui ya dibuja layout {kind: partition-lanes, by: <campo del nodo>} (una columna por valor del campo, titulo = valor; la actividad UML sigue con data.partition). sldb/src/sldb/notations/notation_constants.py LAYOUT_KINDS no lo acepta hoy ('graph','tree','lanes','grid','axis','manual'). Pedido: añadir 'partition-lanes' y el campo opcional 'by' del layout de NotationDoc, y pasarlos tal cual en la vista resuelta. BPMN y la notacion de capas de specIR lo necesitan.

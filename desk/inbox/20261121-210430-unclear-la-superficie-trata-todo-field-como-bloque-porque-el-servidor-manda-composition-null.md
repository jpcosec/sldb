---
sldb:
  by: agent
  at: '2026-11-23T17:58:38Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T21:04:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:58:15'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-sldb-serve-manda-composition-de-cada-field-y-expone-por-modelo-la-ruta-y-la-cardinalidad-create-resp
  (sesion de minegocio, triaje 2026-11-23); el lector de surface la referencia cuando
  toca su pantalla
# conversation thread/message the note came from, e.g. #hilo/1234
---

# La superficie trata todo field como bloque porque el servidor manda composition null

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21, copia de sldb/surface en el commit 562847e2 contra el sldb serve del mismo checkout): GET /document/segments entrega cada field con 'composition': null, 'projection': null y 'table_data': null. La superficie decide si un field es bloque con 'segment.composition !== undefined' (src/core/layout.ts:38, src/react/DocumentSurface.tsx:74, src/views/ComposerView.tsx:22). Esperado: los fields inline del frontmatter salen como filas con su field. Real: todos los fields se tratan como bloque y las filas del frontmatter quedan sin piezas (rows[].pieces = []). Reproducible con cualquier documento con frontmatter tipado; las pruebas de core no lo ven porque sus fixtures no traen la clave en null. En la copia de minegocio se cambio a '!= null'. Pedido: decidir en el contrato si la ausencia se expresa con null o con clave ausente y alinear servidor y superficie.

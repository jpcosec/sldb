---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: minegocio
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T21:04:30'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# La superficie trata todo field como bloque porque el servidor manda composition null

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21, copia de sldb/surface en el commit 562847e2 contra el sldb serve del mismo checkout): GET /document/segments entrega cada field con 'composition': null, 'projection': null y 'table_data': null. La superficie decide si un field es bloque con 'segment.composition !== undefined' (src/core/layout.ts:38, src/react/DocumentSurface.tsx:74, src/views/ComposerView.tsx:22). Esperado: los fields inline del frontmatter salen como filas con su field. Real: todos los fields se tratan como bloque y las filas del frontmatter quedan sin piezas (rows[].pieces = []). Reproducible con cualquier documento con frontmatter tipado; las pruebas de core no lo ven porque sus fixtures no traen la clave en null. En la copia de minegocio se cambio a '!= null'. Pedido: decidir en el contrato si la ausencia se expresa con null o con clave ausente y alinear servidor y superficie.

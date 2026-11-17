---
sldb:
  by: agent
  at: '2026-11-17T02:18:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T22:34:38'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:17:44'
---

# save_document_payload y apply_batch update borran en silencio contenido que el modelo no declara (WS47 del drawer de deskops)

_Describe the incoming message with enough evidence to triage._

Pedido que sale del triaje del drawer de deskops (plan workspace-documental, nodo WS47; ficha desk/drawer/tasks/workspace-documental/task-ws47.md en deskops). En sldb, save_document_payload, y el update de apply_batch que pasa por él (transaction_ops.py), re-renderiza el documento desde el payload sin mirar el archivo previo. refuse_structural_noise y refuse_undeclared_frontmatter solo se aplican al crear o trackear. Si el archivo actual trae ruido estructural o frontmatter que el modelo no declara, una escritura por campos lo borra sin aviso. Pasa a ser real porque la edición por campos de graph_ui va a escribir por apply_batch update. Pedido: que la escritura por campos falle nombrando lo que se perdería y deje el archivo intacto (misma guarda que al crear), con test. Archivos probables: src/sldb/api/documents/payload_save.py, payload_save_steps.py, refuse_structural_noise.py y frontmatter_keys.py. Ninguna tarea activa de sldb lo cubre (revisado 2026-11-16).

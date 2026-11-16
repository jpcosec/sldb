---
sldb:
  by: agent
  at: '2026-11-16T08:16:59Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: proyectos
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-31T03:37:14'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:16:56'
---

# Resiliencia en carga de store ante documentos invalidos y problems estructurados

_Describe the incoming message with enough evidence to triage._

Durante la integracion del Workspace multiproyeccion en graph_ui, se evidencio que load_runtime_documents aborta con ValidationError para todo el store si un solo archivo markdown es invalido, afectando a documentos sanos e impidiendo que el error nombre al archivo culpable. Se sugiere: 1) carga tolerante que aísle documentos invalidos, 2) resolve_runtime_doc focalizado sin barrido total, y 3) estructurar EdgeIndex.problems.

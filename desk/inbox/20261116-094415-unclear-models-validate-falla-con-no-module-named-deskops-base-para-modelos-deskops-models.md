---
sldb:
  by: agent
  at: '2026-11-17T02:01:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T09:44:15'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:01:06'
---

# models validate falla con No module named 'deskops.base' para modelos deskops.models:*

_Describe the incoming message with enough evidence to triage._

Desde UIs/sldb-ui (robocop2, sldb d118e53a): 'python -m sldb models validate PillDoc --format json' -> 'Unexpected: No module named deskops.base' (exit 1). Igual con AtomDoc (deskops.crossroad), Task*Doc (deskops.task), ProtoAtomDoc/MaterializationContractDoc (deskops.atom), y en un store nuevo con solo AtomDoc. deskops.models:AtomDoc sí importa (extract/render/validate/docs create funcionan), así que parece que models validate resuelve los imports relativos del fuente del modelo contra 'deskops.' en vez de 'deskops.models.'. Pasan CrossroadDoc, DeskFAQDoc, InboxNoteDoc, RepositoryDoc, RoleDoc, RunDoc, StepDoc. Otros huecos vistos en el mismo rebase: (a) 'inbox --show <inexistente>' escribe el error por stdout con exit 1; (b) 'inbox <msg> --store <dir sin .sldb>' no falla y escribe en desk/inbox/ del directorio padre; (c) 'fields update/append' no aceptan --format. Evidencia: UIs/sldb-ui runs/rebase-20261116.md (H1, H5, H6, H3). Origen: task-ui-rebase-sldb-actual.

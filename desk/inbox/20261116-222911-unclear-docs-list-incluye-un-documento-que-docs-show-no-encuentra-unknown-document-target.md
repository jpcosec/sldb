---
sldb:
  by: agent
  at: '2026-11-17T02:17:37Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T22:29:11'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:17:03'
---

# docs list incluye un documento que docs show no encuentra (Unknown document target)

_Describe the incoming message with enough evidence to triage._

En el store de UIs/sldb-ui (robocop2), 'docs list --format json' devuelve 'edge-task-v8-link-resolver-scan-classify-resolve-recover-execution-to-activate', pero 'docs show' de ese nombre da 'Unknown document target' (500 en /api/docs/<name>). Ese nombre no está en .sldb/core/store_index.yaml. Lo detectó el tester de task-ui-v3-document-manager (runs/subagents/20261116-v3-t1/result-summary.md). Pregunta: ¿docs list lee de otra fuente que docs show (por ejemplo store.yaml include o un índice derivado)? Las dos deberían coincidir, o docs list debería marcar la entrada como no resoluble.

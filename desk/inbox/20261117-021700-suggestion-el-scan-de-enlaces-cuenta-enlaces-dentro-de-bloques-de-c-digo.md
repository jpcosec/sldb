---
sldb:
  by: agent
  at: '2026-11-17T06:38:54Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T02:17:00'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T03:38:28'
---

# El scan de enlaces cuenta enlaces dentro de bloques de código

_Describe the incoming message with enough evidence to triage._

En sldb-ui (robocop2), el ejecutor de task-ui-v8-link-resolver vio que el scan de enlaces de un doc real lista 'target' dos veces como enlace roto. Los dos casos vienen de ejemplos dentro de bloques de código del markdown, no de enlaces reales. Evidencia: runs/subagents/20261117-v8-e1/result-summary.md en UIs/sldb-ui. Pedido: que el parser de enlaces ignore el contenido de bloques de código (fenced y, si aplica, inline code).

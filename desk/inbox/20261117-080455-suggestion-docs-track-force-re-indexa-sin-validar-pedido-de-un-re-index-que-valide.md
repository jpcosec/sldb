---
sldb:
  by: agent
  at: '2026-11-17T11:20:11Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-17T08:04:55'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T08:19:45'
---

# docs track --force re-indexa sin validar: pedido de un re-index que valide

_Describe the incoming message with enough evidence to triage._

En sldb-ui (robocop2, sldb 472f1c80), el ejecutor de la tarea de track --force midió que 'docs track --force' sobre un doc ya trackeado devuelve rc 0 aunque el archivo no valide: con un enum inválido (five_wh_one_plus) y con frontmatter YAML roto queda indexado, y después 'docs show' falla. Coincide con el código: --force es 'Skip the round-trip check' y track_document_file solo corre _refuse_unfit sin force. Por eso la UI sigue guardando con untrack + track (5.5–6.2 s, contra 4–5 s de --force) para no aceptar documentos inválidos. Pedido: un re-index que valide, por ejemplo 'docs track --reindex' o un --force que solo salte el chequeo de ruta y no el de validez. Evidencia: runs/subagents/20261117-trackforce-e1/validation.log (sondas P1–P7) en UIs/sldb-ui.

---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T16:10:13'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# fields update parsea el valor como YAML y el inbox no tiene promote (matriz UX de sldb-ui)

_Describe the incoming message with enough evidence to triage._

Dos hallazgos de la re-medición de la matriz UX de sldb-ui (runs/ux-stress-20261116/, d2cfea2), que caen del lado del CLI: (1) 'sldb fields update docs/<doc>/<field> <valor>' interpreta el valor como YAML, así que un texto con ': ' (p. ej. 'Uno: dos') falla con un error de validación de pydantic; la UI puede citarlo, pero un valor de texto debería poder pasarse literal (por ejemplo con un flag --string o --raw). (2) 'sldb inbox' no tiene promote, lo que corta la cadena C5 (inbox -> documento). Además fields update/append no aceptan --format (ya avisado en la nota 20261116-094415).

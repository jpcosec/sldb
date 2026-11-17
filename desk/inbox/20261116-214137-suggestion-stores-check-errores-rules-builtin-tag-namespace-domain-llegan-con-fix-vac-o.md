---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T21:41:37'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# stores check: errores rules/builtin:tag_namespace:domain llegan con fix vacío

_Describe the incoming message with enough evidence to triage._

En el store de UIs/sldb-ui (robocop2), 'python -m sldb stores check --format json' devuelve 10 errores; 5 de ellos, con code rules/builtin:tag_namespace:domain, traen fix: ''. sldb-ui ahora muestra cada error con su fix (task-ui-v1-store-explorer), y para esos cinco solo puede decir 'The CLI did not suggest a fix.'. Pedido: que esa regla sugiera un fix, por ejemplo qué namespace de tag declarar o qué tag cambiar. Evidencia: runs/subagents/20261116-v1-e1/evidence/v1.json en UIs/sldb-ui.

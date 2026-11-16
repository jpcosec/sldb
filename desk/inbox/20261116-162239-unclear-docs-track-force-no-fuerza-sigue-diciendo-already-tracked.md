---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T16:22:39'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# docs track --force no fuerza: sigue diciendo already tracked

_Describe the incoming message with enough evidence to triage._

En sldb-ui (robocop2, sldb d118e53a), guardar un documento hace 'docs track <path> --model M --name N --force' después de reescribir el archivo, y el CLI responde 'Doc <name> already tracked.' (exit != 0) aunque se pase --force; untrack seguido de track sí funciona. Así no hay camino atómico para re-indexar un documento editado (hallazgo N-V3-b, S4, en runs/ux-stress-20261116/v3.md; H2 de runs/rebase-20261116.md). Pregunta: ¿--force debería re-trackear, o el camino correcto es 'docs update' (que recibe datos, no markdown)? Hasta tener respuesta, la UI va a usar untrack + track con rollback del archivo.

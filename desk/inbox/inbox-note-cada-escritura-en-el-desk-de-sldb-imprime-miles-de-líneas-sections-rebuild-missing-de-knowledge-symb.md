---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-09T14:26:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Cada escritura en el desk de sldb imprime miles de líneas Sections rebuild missing de knowledge/symbols

_Describe the incoming message with enough evidence to triage._

Visto por el coordinador de proyecto de SLDB_1 el 2026-11-09. Con deskops desde CC35a (toda escritura por sldb.api.transaction), cada comando que escribe en el desk de sldb (add atom, add materialization, edit task) imprime unas 2500 líneas del tipo "Sections rebuild: doc 'python-sldb-sldb-api-corpus-...' missing at <root>/knowledge/symbols/<id>.md". Los documentos de símbolos están indexados en el store pero no existen en un worktree limpio (son generados). El comando termina bien, pero el ruido tapa el resultado y cuesta IO. Esperado: que la reconstrucción de secciones de la transacción se limite a los documentos que la transacción tocó, o que agrupe los faltantes en una sola línea o un alert.

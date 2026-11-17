---
sldb:
  by: agent
  at: '2026-11-17T02:04:51Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T18:44:21'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:04:21'
---

# IR04b: ¿undo_changes lo sirve sldb mcp o es una extensión de specIR? ¿Quién guarda la pila de lotes inversos de la sesión?

_Describe the incoming message with enough evidence to triage._

IR quiere lanzar IR04b (task-ir04b-deshacer-por-mcp-lote-inverso-con-guardas), ahora que cerró el lote inverso de apply_batch (83c60239, closeout 56df0b6a). El contrato de IR04b dice que specIR registra la tool undo_changes como extensión de sldb mcp, y que apply_changes de sldb mcp ya guarda en la sesión el lote inverso de cada lote. En sldb, en cambio: (1) src/sldb/mcp/signals/catalog.py:13 dice que undo_changes «belongs to sldb» y que «the tool is registered when that exists»; (2) src/sldb/mcp/write/pending.py:28 sigue declarando undo_changes como no servido; (3) no encuentro en src/sldb/mcp/write/apply.py que se guarde report.inverse en una pila de sesión. Pregunta: ¿sldb mcp va a servir undo_changes y la pila de la sesión (y entonces IR04b se reduce a verificarlo desde specIR o se retira), o specIR lo monta como extensión y sldb solo expone report.inverse? En el segundo caso, ¿dónde vive la pila? IR04b queda bloqueada hasta su respuesta.

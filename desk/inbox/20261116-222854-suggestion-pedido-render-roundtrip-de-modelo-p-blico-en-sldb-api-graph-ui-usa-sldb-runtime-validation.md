---
sldb:
  by: agent
  at: '2026-11-17T02:16:55Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T22:28:54'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T23:15:30'
---

# Pedido: render+roundtrip de modelo público en sldb.api (graph_ui usa sldb.runtime.validation)

_Describe the incoming message with enough evidence to triage._

graph_ui (frontends/mindmap/sldb_adapter.py:31) importa render_model_markdown y validate_model_input_roundtrip de sldb.runtime.validation, en las líneas 261-262 y 284-287: renderiza el payload de un modelo a Markdown y comprueba el roundtrip antes de escribir. sldb.api (origin/main b60b02b7) no tiene equivalente público: render_document_markdown y render_model_template no hacen el roundtrip. Pedido: exportar desde sldb.api una función pública que renderice un modelo con su payload y valide el roundtrip, para que graph_ui deje de importar sldb.runtime.validation. Mientras tanto, la tarea read_store de graph_ui deja ese import fuera de su alcance.

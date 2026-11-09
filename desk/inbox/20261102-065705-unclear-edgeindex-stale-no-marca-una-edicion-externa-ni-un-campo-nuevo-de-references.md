---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-02T06:57:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# EdgeIndex.stale no marca una edicion externa ni un campo nuevo de __references__

_Describe the incoming message with enough evidence to triage._

Observado en ejecución por el Tester de graph_ui (WS13.1), con sldb 77bd6d00 sobre stores temporales; evidencia en UIs/graph_ui/runs/subagents/20261102-ws13-1-correccion/tester-result-summary.md. Editar el Markdown de un documento por fuera de sldb no hace que load_edge_index(...).stale lo liste por sí solo. Tampoco lo hace añadir un campo a __references__ del modelo con reindex_model. El lector de graph_ui rechaza con store_no_preparado cuando stale no está vacío, y por eso en esos casos muestra relaciones atrasadas sin aviso. La docstring de load_edge_index dice que stale nombra los documentos que una escritura externa dejó atrás. Es intake, no propuesta de reparación: graph_ui no leerá formato interno. Decide el repo dueño si es defecto o límite documentado.

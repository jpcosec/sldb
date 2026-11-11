---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-11T08:00:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# EdgeIndex.stale (GO04 d7eefdeb) manda a reconstruir, pero rebuild_edges no resuelve una edición externa

_Describe the incoming message with enough evidence to triage._

Hallado por la integración de graph_ui (wt/deskops-ui, informe runs/subagents/deskops-ui-integration-report.md), 2026-11-11, sldb 84eb7f75. Desde GO04 d7eefdeb, live_stale compara cada archivo trackeado con el source_hash de su shard. Una edición externa de un documento, válida o no, deja el índice stale, y stale aconseja 'run the rebuild'. Pero rebuild_edges da docs_written=0, porque compara con el hash registrado del store, que no se mueve sin re-track. Resultado: stale queda para siempre hasta un track/update, y como stale es global, un consumidor (graph_ui, _relations_state) bloquea el grafo de todos los documentos, también los sanos. Esperado: o rebuild resuelve lo que stale le manda resolver (re-lee y re-registra el hash del archivo editado), o el mensaje de stale nombra la operación correcta (sldb stores update / docs update <doc>). Útil además: stale por documento, para que un consumidor pueda acotar.

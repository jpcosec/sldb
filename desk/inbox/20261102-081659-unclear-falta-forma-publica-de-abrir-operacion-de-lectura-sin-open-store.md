---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-02T08:16:59'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Falta forma publica de abrir operacion de lectura sin open_store

_Describe the incoming message with enough evidence to triage._

Observado en ejecución y lectura, sldb 77bd6d00. indexed_documents lee el índice por entries_of, caché por operación (store/io/documents_index.py:34-40). En un proceso largo, el alta o baja de un documento por otro proceso no se ve hasta que empieza una operación nueva, y la única forma en sldb.api es open_store, que puede migrar. Un listado de solo lectura no debe migrar (WS11 §5.4). graph_ui WS13.2 llama por ello a new_operation de sldb.store.runtime_cache_signature y de sldb.store.documents_hash, funciones sin guion bajo pero fuera de sldb.api, con precedente en sldb_adapter.refresh_for_concurrent_sessions. Evidencia: UIs/graph_ui/runs/subagents/20261102-ws13-2-explorador/renovacion-1/tester-result-summary.md, H1. Es intake, no reparación. Decide el repo dueño si expone una operación pública equivalente.

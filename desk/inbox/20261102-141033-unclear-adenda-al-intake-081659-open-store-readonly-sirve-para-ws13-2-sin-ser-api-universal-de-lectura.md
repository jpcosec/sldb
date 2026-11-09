---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-02T14:10:33'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Adenda al intake 081659: open_store readonly sirve para WS13.2, sin ser API universal de lectura

_Describe the incoming message with enough evidence to triage._

Adenda a 20261102-081659, sldb 77bd6d00. La corrección WS13.2 de graph_ui (147dabb) reemplazó su listado fresco por sldb.api.open_store(store, mode='readonly'). Medido con audit hook sobre un store canónico preparado: 0 escrituras en GET, también en refresco entre procesos, sin importar sldb.store. Límites: el hook no ve sqlite3 ni subprocesos hijos; open_store añade sys.path en memoria; layout no canónico sin ensayar. Esto cubre ese caso, no reemplaza la forma pública pedida en 081659, que sigue abierta. Queda además una brecha: extract_model_data se importa de sldb.runtime.validation, fuera de sldb.api, y sldb.api solo ofrece extract_document_payload, que carga todos los documentos; no hay forma pública de extraer desde bytes ya leídos.

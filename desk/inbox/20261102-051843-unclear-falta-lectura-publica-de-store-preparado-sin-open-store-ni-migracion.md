---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-02T05:18:43'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Falta lectura publica de store preparado sin open_store ni migracion

_Describe the incoming message with enough evidence to triage._

Gap observado por lectura estática de sldb 77bd6d00; no reproducido en runtime. El lector de graph_ui (WS13.1, contrato WS11 §5.4 y H-14) debe leer sin migrar ni reconstruir como efecto de un GET y rechazar de forma observable un store no preparado. load_edge_index y doc_status pasan por open_store (edge_reading.py:28, doc_status.py:25), y open_store llama migrate_store_layout si el store existe (open_store.py:37-38). La comprobación de layout canónico es privada (_already_canonical, store/migration.py:63) y sldb.api no expone una consulta equivalente de solo lectura. EdgeIndex.stale sí permite detectar índices atrasados, pero solo después de pasar por open_store. Consecuencia: un consumidor no puede saber con API pública, antes de llamar, si leer migrará. Es intake, no propuesta de reparación: graph_ui no leerá formato interno ni usará la función privada. Decide el repo dueño.

---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: pron-repair
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T05:31:07'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# pron contra sldb 9f27733f: undo no restaura el hash del mundo y track/untrack pierde el documento (table-77)

_Describe the incoming message with enough evidence to triage._

Desde pron (suite completa, 2026-11-16, sldb 9f27733f, 475 passed / 7 failed). Dos fallas que pron no puede arreglar sin cambiar sldb: (1) Goldens tests/golden/test_16_golden_{conversation,eval,undo_why x2}: al deshacer una escritura, el sello de procedencia de sldb queda en el documento y hash_after ya no vuelve al hash anterior; detalle en el commit ac7d0f5 de pron. (2) tests/world/test_04_store_by_doc_id.py::test_untrack_and_track_take_the_document_out_and_back: tras untrack + track, find_doc (sldb/api/documents/document_lookup.py:39) lanza SLDBError: Doc 'table-77' not found. tests/world/test_10_federation.py::test_a_world_alone_still_works_the_same: find de Reservation con where 'doc ~ "ana"' devuelve 0 en un mundo solo. Repro: en pron, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q -p syrupy tests/world/test_04_store_by_doc_id.py tests/world/test_10_federation.py tests/golden. Pedido: confirmar si es regresión de sldb o un cambio de contrato que pron debe adoptar (y cuál). La tarea de pron task-pron-vuelve-a-verde-contra-sldb-main... queda bloqueada hasta la respuesta.

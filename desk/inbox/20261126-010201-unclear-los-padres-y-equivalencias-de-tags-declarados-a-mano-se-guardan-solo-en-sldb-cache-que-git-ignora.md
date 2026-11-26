---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-26T01:02:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# los padres y equivalencias de tags declarados a mano se guardan solo en .sldb_cache, que git ignora

_Describe the incoming message with enough evidence to triage._

Hallazgo de la revisión del modelo (2026-11-25). `sldb semantic parent add` y `semantic equivalent add` escriben en .sldb_cache/semantic_dag.yaml (src/sldb/api/semantic/dag_writes.py, src/sldb/store/semantic_dag_sync.py), y .sldb_cache no se versiona. En el store de sldb no hay ninguno declarado. Sin verificar: que borrar la caché los pierda (no se borró), y si algún otro store del workspace tiene alguno. Pedido: verificar las dos cosas y, si se pierden, que esa declaración viva en un archivo versionado. Conviene antes de cualquier cambio de ids.

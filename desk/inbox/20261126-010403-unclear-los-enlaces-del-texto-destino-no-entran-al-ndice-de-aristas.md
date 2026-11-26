---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-26T01:04:03'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# los enlaces del texto ([[destino]]) no entran al índice de aristas

_Describe the incoming message with enough evidence to triage._

Hallazgo de la revisión del modelo (2026-11-26). Los enlaces escritos en el texto de un documento (`[[destino]]`, `[predicado:: [[destino]]]`, `![[doc]]`) los lee solo el paquete src/sldb/links, usado por `docs recover`, `docs compose`, `docs batch`, `lint` y `move`. El índice de aristas no los tiene: una consulta al grafo no ve esos enlaces. `tools/check_axes.py --units` marca `links` como capacidad sin superficie. Pedido: decidir si un enlace del texto es una arista del grafo. Contexto: desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md.

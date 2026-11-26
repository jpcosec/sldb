---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-26T00:17:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# hay tres vocabularios para el tipo de un enlace: predicates del store, RelationTypeDoc y los atributos del modelo

_Describe the incoming message with enough evidence to triage._

Hallazgo de la revisión del modelo (2026-11-26). El tipo de un enlace entre dos cosas se declara en tres lugares: `predicates` de .sldb/store.yaml (para los enlaces del texto, `[predicado:: [[destino]]]`, grupo `sldb predicates`), los documentos `RelationTypeDoc` (aristas autoradas) y los atributos del modelo (`__references__`, `__containment__`, `__compositions__`). No se verificó cómo se relacionan entre sí. Pedido: decir si son uno solo o tres, antes de escribir la taxonomía. Contexto: desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md.

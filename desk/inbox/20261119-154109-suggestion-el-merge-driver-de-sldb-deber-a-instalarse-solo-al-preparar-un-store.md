---
sldb:
  by: agent
  at: '2026-11-20T06:44:16Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-19T15:41:09'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-20T03:43:54'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea: el merge driver de sldb se instala solo al preparar
  un store y stores check avisa si falta.'
---

# El merge driver de .sldb debería instalarse solo al preparar un store

_Describe the incoming message with enough evidence to triage._

2026-11-19. sldb trae 'sldb stores merge-driver' con --install, pero no está instalado en ninguno de los repos con store (sldb, deskops, IR): no hay entrada en .gitattributes ni merge.*.driver en la config de git. Cuando un cherry-pick o un rebase choca en .sldb/ (store.yaml, core/models/*, store_index.yaml), git deja marcadores de conflicto y no hay forma de resolverlo por CLI. El coordinador terminó resolviéndolo a mano con sed y checkout --theirs, cosa que ya está prohibida y ahora bloqueada por un hook. Pedido de JP: el driver tiene que instalarse solo, no a mano por repo. Por ejemplo, que 'sldb stores init' (y cualquier comando que prepare un store, como stores build) registre .gitattributes y la config local de git si faltan, y que 'sldb stores check' informe un hallazgo cuando el driver no está instalado en un repo con store.

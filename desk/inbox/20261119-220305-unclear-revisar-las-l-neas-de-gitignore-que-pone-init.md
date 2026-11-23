---
sldb:
  by: agent
  at: '2026-11-23T01:41:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: hbc_latina
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-19T22:03:05'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T22:40:58'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en la tarea task-stores-check-avisa-cuando-el-gitignore-del-proyecto-todavia-ignora-sldb-runtime-o-sldb-core-layout-a.
  Sigue en 6ab01b80: _OLD_SPLIT solo lo usa migrate-layout, y ni init ni check avisan.
  La parte de .deskops.log es de deskops, que tiene su propia nota (deskops inbox
  20261119-220154).'
---

# revisar las líneas de .gitignore que pone init

_Describe the incoming message with enough evidence to triage._

Hay que revisar qué deja init en el .gitignore del proyecto. Visto en hbc_latina el 2026-11-19: (1) stores init (ensure_cache_ignored) agrega solo .sldb_cache/; .deskops.log, que deskops escribe en la raíz del repo en cada comando, queda sin ignorar y hubo que agregarlo a mano (ver también la nota en el inbox de deskops: 20261119-220154-suggestion-init-no-ignora-deskops-log). (2) Los repos inicializados antes de c420809c (2026-11-04) siguen con .sldb/runtime/ en su .gitignore, por ejemplo heyantonia/plantilla_cliente, que además lo hereda a los repos que genera, y nada avisa hasta que alguien corre stores migrate-layout. Habría que decidir si doctor o init detectan esas líneas viejas y quién es dueño de las líneas de .gitignore de deskops.

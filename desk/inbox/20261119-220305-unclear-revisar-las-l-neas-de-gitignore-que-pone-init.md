---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: hbc_latina
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-19T22:03:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# revisar las líneas de .gitignore que pone init

_Describe the incoming message with enough evidence to triage._

Hay que revisar qué deja init en el .gitignore del proyecto. Visto en hbc_latina el 2026-11-19: (1) stores init (ensure_cache_ignored) agrega solo .sldb_cache/; .deskops.log, que deskops escribe en la raíz del repo en cada comando, queda sin ignorar y hubo que agregarlo a mano (ver también la nota en el inbox de deskops: 20261119-220154-suggestion-init-no-ignora-deskops-log). (2) Los repos inicializados antes de c420809c (2026-11-04) siguen con .sldb/runtime/ en su .gitignore, por ejemplo heyantonia/plantilla_cliente, que además lo hereda a los repos que genera, y nada avisa hasta que alguien corre stores migrate-layout. Habría que decidir si doctor o init detectan esas líneas viejas y quién es dueño de las líneas de .gitignore de deskops.

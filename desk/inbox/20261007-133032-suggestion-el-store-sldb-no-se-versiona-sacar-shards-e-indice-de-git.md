---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-10-07T13:30:32'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# El store .sldb no se versiona: sacar shards e indice de git

_Describe the incoming message with enough evidence to triage._

Decision del dueno (2026-10-07): en sldb, los shards de documentos (.sldb/core/documents/, 1551 archivos) y el indice (.sldb/core/store_index.yaml) NO deben ir en git; hoy estan versionados. Pendiente de definir si core/models/ (35 indices de modelo) tambien sale. Antes de sacarlos hace falta una receta de reconstruccion en un clon limpio: los 1368 documentos de knowledge/ se regeneran con 'sldb selfdoc sync' y 'python-sync'; los otros 183 (docs del repo, desk, inbox) solo los conoce hoy el indice, asi que hace falta declarar modelo y patron de rutas (como kimun.include.edn en kimun) y un script que corra models add + docs track + selfdoc sync. Prueba requerida: reconstruir en un directorio aparte y comparar los 1551 payloads contra el store actual antes de borrar nada. Despues: git rm --cached de lo que salga y .sldb/ en .gitignore salvo README.md. No se ejecuta ahora: el foco esta en kimun (decision 18: v1 sigue en v1).

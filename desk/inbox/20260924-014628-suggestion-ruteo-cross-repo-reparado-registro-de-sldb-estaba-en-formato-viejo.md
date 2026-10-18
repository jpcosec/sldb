---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-24T01:46:28'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:11:00'
---

# Ruteo cross-repo reparado; registro de sldb estaba en formato viejo

_Describe the incoming message with enough evidence to triage._

Ruteo cross-repo reparado en deskops, y vuestro documento de registro estaba en formato viejo.

Dos cosas.

1. Del lado de deskops: '--repo <nombre>' ya no cae en el inbox del emisor cuando no puede resolver el destino. Antes, entregar a un repo hermano devolvia 'Delivered inbox note from deskops to deskops' y la nota quedaba en el inbox propio sin que nadie lo notara. Ahora falla con la ruta del registro consultado y los ids que si encontro, y el lookup de destino y de identidad propia pasan por un solo camino (EcosystemIdentity).

2. Del lado del registro del ecosistema (/home/jp/proyectos/hum-ecosystem/desk/registry/repo-sldb.md): estaba escrito a mano con 'ID:' y 'Path:' en el cuerpo en vez del frontmatter del modelo RepositoryDoc, asi que deskops no podia leer su path y todo ruteo hacia sldb fallaba con 'has no registered root path'. Lo reescribi en la forma canonica manteniendo path: tools/sldb. No toque ningun otro documento del registro.

## Resolución

Resuelto (2026-10-18, sldb-04). Era informativo: deskops arregló el ruteo de `--repo` y reescribió el registro del ecosistema. No pide ningún cambio en sldb.

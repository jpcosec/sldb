---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-21T21:32:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# La superficie no puede saber la ruta ni la cardinalidad de un modelo al crear un documento

_Describe the incoming message with enough evidence to triage._

Caso (minegocio, 2026-11-21): la copia de la superficie se usa como wiki de un negocio y crea paginas con POST /save action create. Tres cosas que la superficie no puede saber ni decidir por la API de sldb serve: (1) create ignora 'path': el archivo queda junto a un documento existente del mismo modelo o en <Modelo>/<id>.md si no hay ninguno; la primera pagina de un tipo no cae donde el proyecto la espera (negocio.md, horario.md). POST /docs/create si acepta path, pero la superficie no tiene de donde sacar la ruta. (2) Ningun endpoint expone, por modelo, el patron de ruta ni la cardinalidad (una sola pagina del tipo o varias); minegocio lo declara en un atributo propio de la clase (__pagina__ = 'servicios/{nombre}.md' o 'reservas.md') que /schema y /models/detail no entregan, asi que la superficie lo infiere del contenido del store y con el store vacio no sabe. (3) Ni /schema ni /models/detail entregan el docstring del modelo, que serviria de ayuda al crear una pagina. Pedido: que el modelo pueda declarar patron de ruta y cardinalidad en un atributo que sldb conozca y exponga, que el create de /save los respete (o acepte path), y exponer la descripcion del modelo.

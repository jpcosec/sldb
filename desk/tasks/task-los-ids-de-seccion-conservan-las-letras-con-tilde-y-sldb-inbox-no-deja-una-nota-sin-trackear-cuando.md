---
sldb:
  by: agent
  at: '2026-11-23T01:39:21Z'
  authority: generated
  via: save_document_payload
id: task-los-ids-de-seccion-conservan-las-letras-con-tilde-y-sldb-inbox-no-deja-una-nota-sin-trackear-cuando
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-185439-suggestion-stores-check-filtrado-por-modelo-y-docs-update-parcial.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los ids de sección conservan las letras con tilde y sldb inbox no deja una nota sin trackear cuando falla el import del modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261122-185439 (pedido de Chatbot_Infra del 2026-11-04, reenviado en 6ab01b80), puntos 3 y 4, que siguen en origin/main 6ab01b80. (3) _slugify de src/sldb/api/records/utils.py usa re.sub(r'[^a-z0-9]+', '-', ...), así que 'Qué hace y para quién' da 'qu-hace-y-para-qui-n'. (4) create_note (src/sldb/cli/commands/inbox_create.py) escribe el archivo con write_note_file antes de auto_track_note; si el import del modelo falla (sin --pythonpath a deskops), la nota queda escrita y sin trackear. Los puntos 1 y 2 (stores check --model y docs update --merge) van en la tarea hermana creada en el mismo triaje, 'stores check filtra por modelo y docs update acepta un payload parcial'.

## Goal

_Describe the concrete result this task must produce._

Los ids de sección conservan las letras Unicode: 'Qué hace y para quién' da 'qué-hace-y-para-quién', o la forma con acentos que ya use src/sldb/links/render.py::_slug; se elige una sola regla para ambos. Y sldb inbox no deja archivo si no puede trackear la nota: o valida y resuelve el modelo antes de escribir, o borra lo escrito y sale con error.

## Scope

_State what is in scope and what is out of scope._

Dentro: src/sldb/api/records/utils.py (_slugify), y src/sldb/links/render.py (_slug) si hay que unificar; src/sldb/cli/commands/inbox_create.py (orden escribir/trackear); tests en tests/test_document_segments.py o un archivo hermano para el slug, y en tests/cli/ para inbox; CHANGELOG.md. Antes de cambiar el slug, buscar con grep quién guarda o compara ids de sección (anclas en links, segmentos, serve), y anotar en el informe si algún índice guardado necesita stores build. Fuera: stores check --model y docs update --merge.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Tests: slug con tildes y ñ; sldb inbox con un modelo que no importa no deja archivo en el inbox. 2) Slug Unicode con \w en vez de [a-z0-9]. 3) inbox: resolver el modelo antes de write_note_file o deshacer la escritura si falla el track. 4) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; la suite completa sale rc 0.

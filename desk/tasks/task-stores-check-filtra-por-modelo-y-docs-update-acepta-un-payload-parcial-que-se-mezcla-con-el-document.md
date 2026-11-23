---
sldb:
  by: agent
  at: '2026-11-23T01:40:30Z'
  authority: generated
  via: save_document_payload
id: task-stores-check-filtra-por-modelo-y-docs-update-acepta-un-payload-parcial-que-se-mezcla-con-el-document
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

# stores check filtra por modelo y docs update acepta un payload parcial que se mezcla con el documento

## Rationale

_Explain why this task exists or the business driver behind it._

Nota desk/inbox/20261122-185439 (pedido de Chatbot_Infra del 2026-11-04, reenviado en 6ab01b80), puntos 1 y 2, que siguen en origin/main 6ab01b80. (1) 'sldb stores check --help' no tiene --model: para chequear solo los modelos de la wiki hay que filtrar el JSON por subject, porque el resto del store (deskops) trae sus propios hallazgos. (2) 'sldb docs update --help' no tiene --merge: un payload parcial falla con campos requeridos. Los puntos 3 y 4 van en la tarea hermana creada en el mismo triaje, 'Los ids de sección conservan las letras con tilde y sldb inbox no deja una nota sin trackear'.

## Goal

_Describe the concrete result this task must produce._

'sldb stores check --model <Modelo>' (repetible) devuelve solo los hallazgos cuyo subject es un documento de esos modelos, o el modelo mismo. 'sldb docs update <doc> --merge' toma el payload actual del documento, le aplica las claves del payload dado (solo el primer nivel) y guarda el resultado con la validación y las reglas de siempre.

## Scope

_State what is in scope and what is out of scope._

Dentro: el parser y el comando de stores check (src/sldb/cli/parsers/stores.py y el comando correspondiente), el filtro en el reporte; el parser y el comando de docs update, con la mezcla antes de save_document_payload (src/sldb/api/documents/payload_save.py); tests en tests/store/test_cli_store.py y tests/api/test_api_documents.py; la referencia del CLI regenerada con selfdoc si el árbol del CLI está documentado; CHANGELOG.md. Fuera: mezcla profunda de listas o diccionarios anidados.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Tests de ambos flags. 2) --model filtra después de calcular el reporte, sin cambiar el cálculo. 3) --merge lee runtime_document, hace dict update y guarda. 4) sldb selfdoc check si aplica. 5) Commit con el trailer 'Task-Id: <id de esta tarea>' en el cuerpo; CHANGELOG.md con una línea en español bajo el encabezado 0.1.13 sin publicar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -p no:cacheprovider tests/store/test_cli_store.py tests/api/test_api_documents.py
- TMPDIR=/dev/shm pytest -n 4 -q -p no:cacheprovider

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; selfdoc check sin diferencias en el árbol del CLI; la suite completa sale rc 0.

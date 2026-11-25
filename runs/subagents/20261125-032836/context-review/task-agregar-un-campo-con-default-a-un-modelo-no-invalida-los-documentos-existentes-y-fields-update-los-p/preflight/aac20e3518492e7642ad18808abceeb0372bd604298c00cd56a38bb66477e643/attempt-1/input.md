FILE:desk/tasks/task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p.md
---
sldb:
  by: agent
  at: '2026-11-25T01:25:48Z'
  authority: generated
  via: save_document_payload
id: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-204955-unclear-agregar-un-campo-con-default-a-un-modelo-invalida-los-documentos-existentes-y-fields-update-no-los-repara.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Agregar un campo con default a un modelo no invalida los documentos existentes y fields update los puede reparar

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261121-204955-unclear-agregar-un-campo-con-default-a-un-modelo-invalida-los-documentos-existentes-y-fields-update-no-los-repara (sesion de minegocio, 21-nov): al agregar un campo de frontmatter con default (espera_segundos: int = 4 con su marcador rev) a un StructuredNLDoc registrado, los documentos existentes quedan store/doc-invalid (input None) y sldb fields update docs/asistente/espera_segundos 4 falla igual porque valida el documento antes de escribir; la unica salida fue editar el Markdown a mano.

## Goal

_Describe the concrete result this task must produce._

Un documento sin la clave nueva toma el default del modelo al extraer y sigue valido.

## Scope

_State what is in scope and what is out of scope._

Extraccion de frontmatter con defaults y un test. Fuera: fields update, migraciones sin default.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: modelo registrado, documento existente, se agrega un campo con default; el documento sigue valido y trae el default. 2) Extraccion que aplica el default ausente. Correr solo el test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_campo_con_default.py

## Done When

_Name the observable condition that makes the task complete._

El test del campo con default pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


---
sldb:
  by: agent
  at: '2026-11-23T17:55:42Z'
  authority: generated
  via: save_document_payload
id: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

Un documento sin la clave nueva toma el default del modelo al extraer y sigue valido; y fields update puede escribir un campo en un documento hoy invalido cuando la escritura lo deja valido.

## Scope

_State what is in scope and what is out of scope._

Extraccion de frontmatter con defaults y validacion previa de fields update en sldb, con tests. Fuera: migraciones de modelos con campos sin default.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: modelo registrado, documento existente, se agrega un campo con default; el documento sigue valido. 2) Test: documento invalido que fields update repara. 3) Extraccion que aplica el default ausente. 4) fields update valida el resultado, no el estado previo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q -n 4 tests/

## Done When

_Name the observable condition that makes the task complete._

Los dos tests pasan y la suite de extract y fields sigue verde.

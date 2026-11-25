Task: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
Title: Agregar un campo con default a un modelo no invalida los documentos existentes y fields update los puede reparar
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-25T03:50:21Z'
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

1) Test NUEVO tests/test_campo_con_default.py: un StructuredNLDoc minimo registrado en un store temporal, un documento escrito; se agrega al modelo el campo espera_segundos: int = 4 con su marcador rev; al re-extraer, el documento no esta en store/doc-invalid y su payload trae espera_segundos == 4. 2) Arreglo en la extraccion para aplicar el default de un campo ausente. Correr solo ese test. (fields update queda en la tarea hermana task-fields-update-repara-un-documento-hoy-invalido-cuando-la-escritura-lo-deja-valido.)

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_campo_con_default.py

## Done When

_Name the observable condition that makes the task complete._

El test del campo con default pasa.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-f58e82999753"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-f58e82999753`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-f58e82999753

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

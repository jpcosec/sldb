Task: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
Title: Agregar un campo con default a un modelo no invalida los documentos existentes y fields update los puede reparar
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T05:51:50Z'
  authority: generated
  via: save_document_payload
id: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-1a73125cf1c4"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.

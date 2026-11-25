---
sldb:
  by: agent
  at: '2026-11-25T01:26:14Z'
  authority: generated
  via: create_document
id: task-fields-update-repara-un-documento-hoy-invalido-cuando-la-escritura-lo-deja-valido
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes-y-fields-update-los-p
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# fields update repara un documento hoy invalido cuando la escritura lo deja valido

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de minegocio (sldb 61c5847f). Partida en 2 tareas chicas al replanificar en DAG (JP 2026-11-24).

## Goal

_Describe the concrete result this task must produce._

fields update valida el resultado de la escritura, no el estado previo: puede escribir un campo en un documento invalido si con eso queda valido.

## Scope

_State what is in scope and what is out of scope._

La validacion previa de fields update y un test. Fuera: extraccion con defaults.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: documento invalido por un campo faltante que fields update repara. 2) Validar el resultado. Correr solo el test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_fields_update_repara.py

## Done When

_Name the observable condition that makes the task complete._

El test de reparacion por fields update pasa.

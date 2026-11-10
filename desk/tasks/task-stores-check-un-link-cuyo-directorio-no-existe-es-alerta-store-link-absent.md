---
sldb:
  by: agent
  at: '2026-11-10T04:56:17Z'
  authority: generated
  via: create_document
id: task-stores-check-un-link-cuyo-directorio-no-existe-es-alerta-store-link-absent
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# stores check: un link cuyo directorio no existe es alerta store/link-absent

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de deskops corre sldb stores check (vía deskops doctor y ci-knowledge-check) sin los repos hermanos enlazados; un link a un directorio inexistente daba store/link-broken (error) y dejaba el CI rojo. Segunda mitad de la decisión (b), revisable, tras task-stores-build-un-store-enlazado-ausente-es-alerta-no-error-build-check-en-ci.

## Goal

_Describe the concrete result this task must produce._

stores check reporta un link cuyo directorio no existe como alerta store/link-absent con nombre y ruta; not-a-store sigue siendo store/link-broken (error).

## Scope

_State what is in scope and what is out of scope._

src/sldb/api/stores/store_surroundings.py y sus tests; sin cambio en deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest -q tests/api/test_unlink_store.py
- pytest -q tests/api/test_inherit_model.py

## Done When

_Name the observable condition that makes the task complete._

Código en main de sldb con tests verdes; stores check sobre un clon limpio de deskops sin hermanos da exit 0 con alertas.

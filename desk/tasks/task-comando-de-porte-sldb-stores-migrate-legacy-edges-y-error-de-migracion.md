---
id: task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion
current_node: checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-execution-ready
history: []
references: []
depends_on:
- task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges
pills: []
files: []
checklists:
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-execution-ready
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-testing-ready
- checklist-task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Comando de porte sldb stores migrate-legacy-edges y error de migracion

## Rationale

_Explain why this task exists or the business driver behind it._

Decision del mantenedor: al retirar runtime/edges/, un store con la capa vieja debe fallar con un error que incluya el link al comando que porta y borra. Sin eso, el retiro deja stores existentes ilegibles sin salida. Especificado en docs/architecture/edges-retirement-plan.md secciones 3 y 4.

## Goal

_Describe the concrete result this task must produce._

Implementar 'sldb stores migrate-legacy-edges' y el error de apertura que lo referencia.

## Scope

_State what is in scope and what is out of scope._

IN: el comando (lee runtime/edges/, escribe el snapshot nuevo, BORRA runtime/edges/, idempotente) y el check en open_store que lanza el error. OUT: el borrado de los modulos de la capa vieja va en la tarea siguiente.

## Implementation Path

_Outline the expected implementation route or affected surface._

Engancha en open_store, al lado de migrate_store_layout (api/stores/open_store.py:36-38). El error es SLDBStoreError con el tono de store_discovery.py:20: diagnostico + comando exacto. El texto literal ya esta redactado en la seccion 4 del plan; usalo.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

El comando porta un store real con runtime/edges/ y lo deja sin esa carpeta; re-ejecutarlo es no-op; abrir un store sin portar da el error con el comando; pytest verde.

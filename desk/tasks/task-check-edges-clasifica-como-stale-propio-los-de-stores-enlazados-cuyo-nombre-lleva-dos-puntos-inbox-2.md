---
sldb:
  by: agent
  at: '2026-11-15T15:52:16Z'
  authority: generated
  via: create_document
id: task-check-edges-clasifica-como-stale-propio-los-de-stores-enlazados-cuyo-nombre-lleva-dos-puntos-inbox-2
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
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# check_edges clasifica como stale propio los de stores enlazados cuyo nombre lleva dos puntos (inbox 20261115-015936)

## Rationale

_Explain why this task exists or the business driver behind it._

En un repo con stores enlazados, sldb edges check reporta cientos de stale propios y ok=False mientras --local da OK.

## Goal

_Describe the concrete result this task must produce._

Clasificar el stale por el store dueño del nodo, no por el conteo de ':'.

## Scope

_State what is in scope and what is out of scope._

Bug del inbox sldb 20261115-015936, verificado hoy en HEAD: check_edges separa linked_stale con un conteo de ':' igual a 2, y un documento de un store enlazado con ':' en su nombre cuenta como propio. Reproducir con un store enlazado cuyo documento lleve ':' en el nombre, antes con caché frío y caliente; corregir clasificando por el store dueño; test de regresión.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

El test de regresión pasa; EdgeCheckReport.ok coincide entre include_linked=False y --local para ese caso; suite de a un archivo, tools/check.sh y stores build --check.

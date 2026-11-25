FILE:desk/tasks/task-higiene-del-desk-de-sldb-cerrar-con-closeout-resolved-by-citando-el-sha-las-tareas-abiertas-cuyo-tra.md
---
sldb:
  by: agent
  at: '2026-11-17T02:43:45Z'
  authority: generated
  via: create_document
id: task-higiene-del-desk-de-sldb-cerrar-con-closeout-resolved-by-citando-el-sha-las-tareas-abiertas-cuyo-tra
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- desk/tasks/Board.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Higiene del desk de sldb: cerrar con closeout resolved-by, citando el sha, las tareas abiertas cuyo trabajo ya está integrado en main

## Rationale

_Explain why this task exists or the business driver behind it._

El board de sldb tiene entre 46 y 49 tareas abiertas y una parte tiene su trabajo ya integrado en origin/main (por otras tareas o por commits sueltos), así que el board no dice qué falta de verdad. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Toda tarea abierta cuyo goal y done_when ya se cumplen en origin/main queda cerrada con deskops closeout en modo resolved-by citando el sha que la resolvió; las que no, siguen abiertas con una línea en el informe que dice por qué.

## Scope

_State what is in scope and what is out of scope._

Entra: recorrer deskops list tasks --root . (abiertas), y para cada una buscar en git log de origin/main y en el código si su goal ya se cumple; si se cumple, cerrarla con el modo resolved-by de deskops closeout (ver deskops closeout --help) citando el sha, con la evidencia que pida el gate; si no, anotarla. Informe en result-summary.md con la tabla tarea -> cerrada (sha) o abierta (motivo). No entra: implementar nada, tocar src/, cerrar tareas a medias.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) deskops list tasks y deskops closeout --help para el modo resolved-by. 2) Para cada tarea, leer su contrato y buscar evidencia en origin/main (git log --grep, git log -S, lectura del código). 3) Cerrar las resueltas una por una con su sha. 4) deskops graph missing en 0. 5) Informe.

## Validation

_List the checks required before this task can close._

- cd .. && TMPDIR=/dev/shm deskops graph missing --root sldb
- cd .. && TMPDIR=/dev/shm deskops list tasks --root sldb

## Done When

_Name the observable condition that makes the task complete._

Cada tarea cerrada cita un sha de origin/main que la resuelve; result-summary.md tiene la tabla completa; deskops graph missing da 0; commit de desk con [skip ci].

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-higiene-del-desk-de-sldb-cerrar-con-closeout-resolved-by-citando-el-sha-las-tareas-abiertas-cuyo-tra: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


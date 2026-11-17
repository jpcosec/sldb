---
sldb:
  by: agent
  at: '2026-11-17T04:08:29Z'
  authority: generated
  via: save_document_payload
id: task-sw8-decisión-de-jp-qué-queda-de-la-superficie-anterior-de-surface-vistas-legacy-stores-demo-y-caso-l
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
- area:surface
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-233957-suggestion-sw8-decisi-n-de-jp-task-decision-qu-queda-de-la-superficie-anterior-de-surface-y-de-sus-stores-demo.md
depends_on: []
pills: []
files:
- docs/surface/tasks/README.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW8, decisión de JP: qué queda de la superficie anterior de surface (vistas legacy, stores demo y caso Levira, T8 identidad de sección)

## Rationale

_Explain why this task exists or the business driver behind it._

Con el Workbench de cuatro vistas (df3903db) quedan partes de la superficie anterior sin destino: vistas legacy (Salud y Bandeja sin equivalente; Lector y Destilación cubiertas en parte), stores demo y código del caso Levira en surface/src/core (una tarea en draft los toca), y T8 (identidad de sección). Hasta que JP decida no se borra nada. Origen: desk/inbox/20261116-233957-suggestion-sw8-decisi-n-de-jp-task-decision-qu-queda-de-la-superficie-anterior-de-surface-y-de-sus-stores-demo.md.

## Goal

_Describe the concrete result this task must produce._

JP decide: (A) qué vistas legacy se retiran y cuáles sobreviven dentro del Workbench; (B) si los stores demo y el código del caso Levira quedan como fixture de desarrollo o se retiran con la maqueta; (C) si T8 sigue como tarea de sldb o se descarta. La decisión queda escrita y de ella salen las tareas de retiro.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar a JP las tres preguntas con lo que hay hoy (sin recomendación vinculante del coordinador), registrar el recibo owner y, cuando JP disponga, crear las tareas de retiro o conservación. No entra: borrar nada antes de la decisión.

Precisión de JP (2026-11-17, prevalece sobre lo anterior): el Workbench de sldb/surface es LA UI de SLDB, general y autónoma para cualquier store SLDB; no es una superficie de la UI de deskops. La §2 del manual (que lo presenta como superficie de deskops) está desactualizada y no es premisa de este contrato. Principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Nada del Workbench depende de que exista un desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de vistas legacy, stores demo y código Levira en surface/src. 2) Presentar las preguntas a JP. 3) Registrar su decisión y crear las tareas.

## Validation

_List the checks required before this task can close._

- ls desk/tasks | grep -i surface

## Done When

_Name the observable condition that makes the task complete._

Recibo owner aceptado por JP con la decisión de A, B y C; existen las tareas que salen de ella.

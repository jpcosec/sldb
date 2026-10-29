---
id: task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field
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
task_type: design
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-atomo-y-field-convergieron-falta-un-set-bootstrap.md
---

# Diseño: set bootstrap de modelos tras la convergencia átomo/field

## Rationale

_Explain why this task exists or the business driver behind it._

La nota del 2026-10-01 muestra que AtomDoc y los fields tienen la misma forma y difieren solo en de dónde sale su identidad, y propone un set bootstrap de siete modelos (Fuente…Modelo). El dueño pidió (2026-10-29) tratarla como tarea de diseño: el entregable es un documento, no código.

## Goal

_Describe the concrete result this task must produce._

Un documento de decisión en docs/ (SpecDoc o PlanDoc trackeado) que evalúe la propuesta de siete modelos, diga qué se adopta, qué no y por qué, con ejemplos de cada modelo sobre documentos reales del store.

## Scope

_State what is in scope and what is out of scope._

Solo documento. Sin cambios de código ni de modelos existentes. Cita la nota original y los átomos relevantes.

## Implementation Path

_Outline the expected implementation route or affected surface._

Un agente redacta la propuesta; el dueño decide sobre el texto.

## Validation

_List the checks required before this task can close._

- sldb docs show <doc> --store .sldb renderiza el documento trackeado

## Done When

_Name the observable condition that makes the task complete._

El documento existe, está trackeado y el dueño marcó en él cada punto como adoptado o rechazado.

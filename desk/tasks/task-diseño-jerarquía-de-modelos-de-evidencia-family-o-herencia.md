---
id: task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia
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
from_drawer: desk/drawer/tasks/task-documentar-el-patron-de-modelo-repo-local-cerrar-el-reporte-de-hash-b-y-definir-la-familia-de-modelos-de-evidencia.md
---

# Diseño: jerarquía de modelos de evidencia (__family__ o herencia)

## Rationale

_Explain why this task exists or the business driver behind it._

La nota del 2026-09-23 dejó abierta la familia de modelos de evidencia después de documentar el patrón repo-local y cerrar hash_b. El dueño pidió (2026-10-29) una tarea de diseño cuyo entregable es un documento.

## Goal

_Describe the concrete result this task must produce._

Un documento de decisión en docs/ que compare __family__ vs herencia de clases para los modelos de evidencia, con la recomendación y sus consecuencias para deskops (RunDoc, materializaciones, closeout_evidence).

## Scope

_State what is in scope and what is out of scope._

Solo documento. Sin cambios de código.

## Implementation Path

_Outline the expected implementation route or affected surface._

Un agente redacta la comparación; el dueño decide.

## Validation

_List the checks required before this task can close._

- sldb docs show <doc> --store .sldb renderiza el documento trackeado

## Done When

_Name the observable condition that makes the task complete._

El documento existe, está trackeado y tiene la decisión del dueño anotada.

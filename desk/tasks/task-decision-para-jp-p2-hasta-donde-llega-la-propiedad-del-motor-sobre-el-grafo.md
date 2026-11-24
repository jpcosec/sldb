---
sldb:
  by: agent
  at: '2026-11-24T07:15:13Z'
  authority: generated
  via: create_document
id: task-decision-para-jp-p2-hasta-donde-llega-la-propiedad-del-motor-sobre-el-grafo
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
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decision para JP P2: hasta donde llega la propiedad del motor sobre el grafo

## Rationale

_Explain why this task exists or the business driver behind it._

El motor Datalog sera duenio del almacenamiento y la consulta de aristas; hoy GraphBackend solo cubre eval y analyze sobre networkx y el indice se compone fuera del backend. Plan: desk/drawer/plans/grafo-datalog-daemon (poc/informe.md).

## Goal

_Describe the concrete result this task must produce._

Fijar el alcance. Opciones: A) el motor es duenio de las aristas y de eval; analyze (path, cycles, order, components, central, similar) migra despues, nodo a nodo, y networkx queda mientras tanto; B) el motor es duenio de todo y networkx se retira (analisis como reglas Datalog; central y similar no son consultas Datalog naturales); C) el motor solo reemplaza el cache de aristas (.sldb_cache) y GraphBackend queda como esta. Recomendacion: A.

## Scope

_State what is in scope and what is out of scope._

Dentro: alcance de la propiedad y orden de migracion. Fuera: eleccion del motor (P1).

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer poc/informe.md y brief.md del plan; JP responde A, B o C; se actualiza G_OWNERSHIP

## Validation

_List the checks required before this task can close._

- JP responde en la tarea; el dag.yaml del plan grafo-datalog-daemon refleja la respuesta

## Done When

_Name the observable condition that makes the task complete._

JP respondio y G_OWNERSHIP tiene la respuesta como evidence.

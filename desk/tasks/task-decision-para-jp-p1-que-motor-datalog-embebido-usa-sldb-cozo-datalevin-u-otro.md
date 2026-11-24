---
sldb:
  by: agent
  at: '2026-11-24T02:23:06Z'
  authority: generated
  via: create_document
id: task-decision-para-jp-p1-que-motor-datalog-embebido-usa-sldb-cozo-datalevin-u-otro
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

# Decision para JP P1: que motor Datalog embebido usa sldb (Cozo, Datalevin u otro)

## Rationale

_Explain why this task exists or the business driver behind it._

JP revirtio D5 el 2026-11-23: el grafo pasa a un motor Datalog duenio de las aristas. Plan: desk/drawer/plans/grafo-datalog-daemon (poc/informe.md). La prueba de concepto corrio con CozoDB.

## Goal

_Describe the concrete result this task must produce._

Elegir el motor. Opciones: A) Cozo (cozo-embedded 0.7.6, cliente Python, Datalog con recursion y negacion estratificada, almacenamiento sqlite o rocksdb; medido: reabrir la base cargada 7 ms, 385 a 552 MB sobre el arranque); B) Datalevin (candidato de docs/architecture/graph-backend.md; sin cliente Python en PyPI, exige JVM o binario y un proceso aparte); C) quedarse en networkx y resolver la recomposicion con cache y daemon, sin motor Datalog. Recomendacion: A, con la salvedad de que la actividad reciente del proyecto Cozo no esta verificada.

## Scope

_State what is in scope and what is out of scope._

Dentro: motor, almacenamiento y dependencia nueva. Fuera: propiedad de eval y analyze (P2), forma del daemon (P3) e invalidacion (P4).

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer poc/informe.md; JP responde A, B o C; se actualiza G_ENGINE del dag.yaml

## Validation

_List the checks required before this task can close._

- JP responde en la tarea; el dag.yaml del plan grafo-datalog-daemon refleja la respuesta

## Done When

_Name the observable condition that makes the task complete._

JP respondio y G_ENGINE tiene la respuesta como evidence.

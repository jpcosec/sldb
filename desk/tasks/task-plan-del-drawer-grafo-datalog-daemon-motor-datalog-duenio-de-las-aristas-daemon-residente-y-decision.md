---
sldb:
  by: agent
  at: '2026-11-24T02:37:49Z'
  authority: generated
  via: save_document_payload
id: task-plan-del-drawer-grafo-datalog-daemon-motor-datalog-duenio-de-las-aristas-daemon-residente-y-decision
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Plan del drawer grafo-datalog-daemon: motor Datalog duenio de las aristas, daemon residente y decisiones para JP, a partir de la prueba de concepto

## Rationale

_Explain why this task exists or the business driver behind it._

Segunda parte de las notas de JP del 2026-11-23 (motor Datalog que revierte D5 y daemon de sldb), separada por atomizacion de task-plan-del-drawer-motor-datalog-duenio-de-las-aristas-revierte-d5-y-daemon-residente-de-sldb-con-prueb, que hace solo la prueba de concepto.

## Goal

_Describe the concrete result this task must produce._

desk/drawer/plans/grafo-datalog-daemon/ con alcance, brief, decisiones y dag.yaml (formato de grafo-operable), apoyado en las mediciones de la prueba de concepto; el daemon cubre que queda residente, como lo encuentra el CLI, que pasa sin daemon en contenedores y tests, invalidacion con git, relacion con sldb serve y hooks, y memoria frente al tope de 8 GB; decisiones.md de grafo-operable registra D5 revertida por JP el 2026-11-23; una task.decision por decision abierta (minimo: motor, forma del daemon, invalidacion).

## Scope

_State what is in scope and what is out of scope._

Solo documentos del drawer y las task.decision. Fuera: codigo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el informe de la prueba de concepto. 2) Escribir el plan. 3) Registrar D5 revertida. 4) Crear las task.decision.

## Validation

_List the checks required before this task can close._

- deskops graph missing --root . sin faltantes nuevos

## Done When

_Name the observable condition that makes the task complete._

El plan existe con dag.yaml legible por deskops review node; D5 aparece revertida con fecha; hay una task.decision por decision abierta.

---
sldb:
  by: agent
  at: '2026-11-24T02:24:30Z'
  authority: generated
  via: create_document
id: task-decision-para-jp-p3-forma-del-daemon-de-sldb-y-que-pasa-sin-el
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

# Decision para JP P3: forma del daemon de sldb y que pasa sin el

## Rationale

_Explain why this task exists or the business driver behind it._

JP pide ver ahora el daemon (diferido desde 2026-11-15). La prueba mostro que reabrir una base persistida cuesta 7 ms y que un indice residente baja 50 consultas sueltas de 49 s a menos de 20 ms. Plan: desk/drawer/plans/grafo-datalog-daemon (poc/informe.md).

## Goal

_Describe the concrete result this task must produce._

Elegir la forma. Opciones: A) un daemon por proyecto en socket Unix bajo .sldb_cache, opcional; sin daemon (contenedores de ejecutor, tests) el cliente abre la base persistida en proceso y, si no existe, compone como hoy; B) sin daemon: solo base persistida abierta en proceso en cada invocacion (7 ms, sin proceso residente que gestionar); C) un daemon unico por usuario con varios proyectos (comparte memoria; mas riesgo con el tope de 8 GB libres de robocop2: 0,4 a 0,6 GB por indice federado de sldb). Recomendacion: A; B ya cubre la carga en frio si JP prefiere no gestionar procesos.

## Scope

_State what is in scope and what is out of scope._

Dentro: forma, descubrimiento del cliente, comportamiento sin daemon, relacion con sldb serve y con los hooks actuales, memoria. Fuera: invalidacion (P4).

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer poc/informe.md; JP responde A, B o C; se actualiza G_DAEMON_SHAPE

## Validation

_List the checks required before this task can close._

- JP responde en la tarea; el dag.yaml del plan grafo-datalog-daemon refleja la respuesta

## Done When

_Name the observable condition that makes the task complete._

JP respondio y G_DAEMON_SHAPE tiene la respuesta como evidence.

---
sldb:
  by: agent
  at: '2026-11-26T23:57:24Z'
  authority: generated
  via: create_document
id: task-evaluar-llevar-kimun-como-core-de-sldb
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
pointers: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Evaluar llevar kimun como core de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 2026-11-26: 'vamos a evaluar llevar kimun como core de sldb'. kimun ya tiene un borrador de ese diseño (kimun docs/v2/drafts/diseno-nucleo-sldb.md, 2026-11-17) con cuatro preguntas al dueño sin contestar, y el spec de producto de sldb se está escribiendo ahora: los dos tienen que decir lo mismo antes de elegir motor (P1) o de ordenar el cambio de ids contra el almacén del motor.

## Goal

_Describe the concrete result this task must produce._

JP tiene escrito, punto por punto del spec de sldb, qué resuelve kimun como núcleo, qué contradice y qué queda en Python, con evidencia medida sobre copias, para decidir si kimun pasa a ser el core de sldb.

## Scope

_State what is in scope and what is out of scope._

Leer kimun (docs/v2/00-nucleo.md, drafts/diseno-nucleo-sldb.md, plan-producto.md, src/kimun) y contrastarlo con docs/spec/ y desk/drawer/plans/spec-de-producto-de-sldb/. Cruces a resolver: (1) kimun 've, sintetiza y genera' y no escribe fuentes, y el spec exige crear, cambiar y borrar en todo nodo y arista; (2) kimun no construye shards, cadena de hashes ni federación, y el spec tiene árbol de hashes, hooks y alertas; (3) el motor es dueño de todo el grafo (JP) y kimun no declara motor Datalog; (4) consumidores Python contra un proceso residente del motor, y su relación con el daemon y el servidor fastmcp; (5) los modelos: clase Python como fuente o declaración del motor. Correr sobre copias las cuatro pruebas del §8 de diseno-nucleo-sldb.md. No implementa ni migra nada.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Cada cruce del scope tiene una respuesta con ruta:línea de kimun y de sldb
- Las cuatro pruebas del §8 tienen resultado medido o dicen por qué no se pudieron correr

## Done When

_Name the observable condition that makes the task complete._

Existe un documento de evaluación con una tabla punto del spec -> kimun (resuelve, contradice, queda en Python) y los resultados de las cuatro pruebas, y JP anotó su decisión.

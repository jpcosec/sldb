---
sldb:
  by: agent
  at: '2026-11-27T03:26:05Z'
  authority: generated
  via: create_document
id: task-refactor-de-sldb-por-anillos-puerta-que-falle-cortar-el-nudo-borrar-y-mover-clean-code
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
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Refactor de sldb por anillos: puerta que falle, cortar el nudo, borrar y mover, clean code

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Que el código de sldb respete el reparto de anillos de docs/spec/mecanismos/anillos.md (confirmado por JP el 2026-11-27): cada anillo importa solo de los de adentro, y una puerta falla si eso se rompe.

## Scope

_State what is in scope and what is out of scope._

Cuatro etapas en un worktree aparte, cada una con su commit: (1) la puerta de ejes falla cuando los ejes no forman un orden de un solo sentido, con las violaciones de hoy como lista de deuda que solo puede bajar, y un tope de tamaño de función y de archivo medido antes de empezar; (2) cortar las dependencias que cierran el nudo de 23 ejes, de las débiles a las fuertes; (3) borrar lo que nadie usa (revisando antes a deskops, IR y graph_ui), unificar duplicados y mover; (4) modularizar: funciones grandes, archivos grandes, clases donde hay funciones sueltas con estado compartido. No toca desk/, .sldb/ ni la documentación vieja. No cambia comportamiento sin un test que lo diga.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- bash tools/check.sh; python -m pytest -q con la misma lista de fallos que antes de empezar o menos; python tools/check_axes.py --dag muestra menos ejes en el nudo que 23

## Done When

_Name the observable condition that makes the task complete._

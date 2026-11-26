---
sldb:
  by: agent
  at: '2026-11-26T03:16:11Z'
  authority: generated
  via: create_document
id: task-plan-del-refactor-del-repo-por-anillos-y-ejes-a-que-anillo-va-cada-modulo-y-que-imports-lo-impiden
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md
---

# Plan del refactor del repo por anillos y ejes: a qué anillo va cada módulo y qué imports lo impiden

## Rationale

_Explain why this task exists or the business driver behind it._

JP propuso el 2026-11-26 ordenar el repo con los mismos anillos y ejes con que se ordenan las operaciones (desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md). Hoy contracts/layers.toml ordena por quién importa a quién y deja api como una sola capa de 363 archivos que tools/check_axes.py --units no reconoce como unidad (fachada); el mismo reporte dice que 6 imports cierran el nudo del núcleo y 26 el de api, y que mientras existan reorganizar carpetas es cosmético. Asignar módulos a anillos además prueba si el corte de anillos es correcto antes de tocar la CLI.

## Goal

_Describe the concrete result this task must produce._

Un plan en desk/drawer/plans/ con su dag.yaml que diga a qué anillo (0 grafo, 1 mantener correcto, 2 store entero, 3 compuesto, caras) pertenece cada módulo de src/sldb, cuántos imports van hoy de un anillo hacia uno más externo, cuáles hay que cortar y en qué orden, y qué movimientos de carpetas quedan después. Solo planifica: no mueve ni edita código.

## Scope

_State what is in scope and what is out of scope._

Leer desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md, contracts/layers.toml, contracts/identity.toml y la salida de tools/check_axes.py --units. Asignar cada módulo de src/sldb/{core,models,runtime,code,notations,store,links,api,cli,mcp,selfdoc} a un anillo, y dentro del anillo 0 a su tipo de nodo o de arista y a navegación. Medir los imports que cruzan hacia afuera con las herramientas de tools/ que ya existen; si falta una medida, pedirla como tarea, no escribir un script suelto. Listar los módulos que no caen claro en ningún anillo como preguntas para JP. Proponer el orden: declarar anillos en contracts/, cortar imports, mover carpetas. Decir qué del plan choca con trabajo sin empujar en robocop2. Fuera de alcance: mover archivos, cambiar imports, tocar la CLI o la taxonomía.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- python tools/check_axes.py --units
- python tools/check_layers.py
- cada módulo de src/sldb aparece en la tabla de asignación del plan o en su lista de preguntas abiertas

## Done When

_Name the observable condition that makes the task complete._

El plan y su dag.yaml están en desk/drawer/plans/, cada módulo de src/sldb tiene anillo o figura como pregunta abierta, el conteo de imports hacia afuera está medido y no estimado, y JP revisó la asignación.

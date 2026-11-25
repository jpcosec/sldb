FILE:desk/tasks/task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra.md
---
sldb:
  by: agent
  at: '2026-11-25T17:43:56Z'
  authority: generated
  via: create_document
id: task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# una NotationDoc declara qué estándar implementa y sldb notations validate lo muestra

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). Un estándar (UML, BPMN, IFML, ORCA) es una notación, pero hoy nada en una NotationDoc dice qué estándar implementa ni en qué versión, así que no se puede listar "las notaciones de BPMN de este store" ni comparar dos notaciones del mismo estándar.

## Goal

_Describe the concrete result this task must produce._

Un campo opcional en la notación con el nombre y la versión del estándar, validado y visible al listar y validar.

## Scope

_State what is in scope and what is out of scope._

Dentro: el modelo NotationDoc, su carga desde YAML (src/sldb/notations/notation_spec.py) y la salida de sldb notations. Fuera: el contenido de ninguna notación (es de specIR), reglas sobre cobertura del estándar.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/notations-and-views.md y tags.md: antes de agregar un campo, comprobar si los tags semánticos de la notación ya pueden llevar el estándar, y elegir el campo solo si no.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_notation_declares_standard.py

## Done When

_Name the observable condition that makes the task complete._

Una notación con el estándar declarado se valida y lo muestra; una sin él sigue siendo válida. Un nombre vacío o una versión sin nombre se rechaza con un mensaje que nombra el campo. La documentación de notaciones describe el campo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


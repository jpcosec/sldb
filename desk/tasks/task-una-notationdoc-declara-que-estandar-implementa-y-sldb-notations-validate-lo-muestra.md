---
sldb:
  by: agent
  at: '2026-11-26T00:33:43Z'
  authority: generated
  via: save_document_payload
id: task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
pointers: []
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

Aclaraciones de la revisión: Primero mirar si los tags semánticos pueden llevar nombre y versión con validación; si no (lo esperable), campo opcional standard: {name: str, version: str | None} en NotationDoc. name obligatorio y no vacío si standard está; version opcional; version sin name o name vacío/solo espacios se rechaza con mensaje que nombra la notación. sldb notations list y validate muestran 'standard: <name> <version>' (y en json el objeto) cuando existe; sin campo, nada. Documentación: docs/architecture/notations-and-views.md. tests/test_notation_declares_standard.py se crea. Va después de la tarea de huecos del resolver (mismas notaciones): parte de main actual. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_notation_declares_standard.py

## Done When

_Name the observable condition that makes the task complete._

Una notación con el estándar declarado se valida y lo muestra; una sin él sigue siendo válida. Un nombre vacío o una versión sin nombre se rechaza con un mensaje que nombra el campo. La documentación de notaciones describe el campo.

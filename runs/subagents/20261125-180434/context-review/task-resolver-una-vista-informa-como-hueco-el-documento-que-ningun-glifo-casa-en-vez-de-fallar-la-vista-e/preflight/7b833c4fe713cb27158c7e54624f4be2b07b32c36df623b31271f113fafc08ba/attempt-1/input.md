FILE:desk/tasks/task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e.md
---
sldb:
  by: agent
  at: '2026-11-25T17:43:19Z'
  authority: generated
  via: create_document
id: task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e
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

# resolver una vista informa como hueco el documento que ningún glifo casa, en vez de fallar la vista entera

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de specIR (desk/drawer/plans/pedidos-de-specir-y-graph-ui/). Hoy un documento que ningún GlyphDoc de la notación casa hace fallar todo el resolve_view con ViewError. Así no se puede medir qué parte de un store cubre una notación, que es lo que hace falta para revisar un estándar (UML, BPMN, IFML, ORCA) como notación.

## Goal

_Describe the concrete result this task must produce._

Que la vista se resuelva con los documentos que sí casan y que el resultado liste aparte los que no, con su id y su modelo.

## Scope

_State what is in scope and what is out of scope._

Dentro: sldb.api.notations (resolve_view, evaluate_projection_view y ViewError) y la ruta de sldb serve que los expone. Fuera: cambiar el formato de NotationDoc, graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/notations-and-views.md. Los huecos van en un campo propio del resultado; un llamador que quiera el comportamiento estricto lo pide de forma explícita.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_view_reports_unmatched_documents.py
- python -m pytest -q tests -k "notation or view"

## Done When

_Name the observable condition that makes the task complete._

Una vista sobre un store con un documento sin glifo devuelve los demás nodos y aristas y lista ese documento como hueco con id y modelo. En modo estricto sigue fallando con el mismo error que hoy. sldb notations validate no cambia.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


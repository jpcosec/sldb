---
sldb:
  by: agent
  at: '2026-11-25T23:14:52Z'
  authority: generated
  via: save_document_payload
id: task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e
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

Aclaraciones de la revisión: Campo gaps en el resultado: lista de {id, model}, donde model es el nombre del modelo del documento (p. ej. TaskCodeDoc). Parámetro strict: bool = False en resolve_view y evaluate_projection_view; con strict=True se conserva exactamente el ViewError de hoy (mismo tipo y mensaje); ViewError no cambia. La ruta de evaluación de vistas de sldb serve (la que llama a evaluate_projection_view, ver src/sldb/cli/serve) devuelve gaps y acepta strict como query param. Sin huecos, gaps es []. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_view_reports_unmatched_documents.py
- python -m pytest -q tests -k "notation or view"

## Done When

_Name the observable condition that makes the task complete._

Una vista sobre un store con un documento sin glifo devuelve los demás nodos y aristas y lista ese documento como hueco con id y modelo. En modo estricto sigue fallando con el mismo error que hoy. sldb notations validate no cambia.

---
sldb:
  by: agent
  at: '2026-11-25T22:07:09Z'
  authority: generated
  via: save_document_payload
id: task-el-layout-de-una-notationdoc-acepta-partition-lanes-con-by-y-la-vista-resuelta-lo-pasa-tal-cual
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

# El layout de una NotationDoc acepta partition-lanes con by y la vista resuelta lo pasa tal cual

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui ya dibuja {kind: partition-lanes, by: <campo>} (una columna por valor del campo, commit 5bee085 de graph_ui) y sldb lo rechaza: LAYOUT_KINDS en src/sldb/notations/notation_constants.py solo admite graph, tree, lanes, grid, axis y manual. BPMN y la notación de capas de specIR lo necesitan. Pedido por inbox de graph_ui (20261125-213030).

## Goal

_Describe the concrete result this task must produce._

Una NotationDoc puede declarar layout {kind: partition-lanes, by: <nombre de campo>} y sldb la valida y la entrega igual en la vista resuelta.

## Scope

_State what is in scope and what is out of scope._

Solo el mecanismo de notaciones de sldb: notation_constants.py (LAYOUT_KINDS), el validador de layout en notation_spec.py y lo que pase el layout a la vista resuelta. No mover notaciones a specIR ni tocar graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Añadir 'partition-lanes' a LAYOUT_KINDS en src/sldb/notations/notation_constants.py. 2) En el validador _layout de src/sldb/notations/notation_spec.py (hoy ya deja pasar las claves que no conoce, y así sigue): si hay 'by', debe ser str y no vacío tras strip(); se guarda recortado. 'by' con un kind distinto de partition-lanes es ValueError 'layout.by only applies to kind partition-lanes'; 'by' vacío o no str es ValueError 'layout.by must be a non-empty field name'. by es opcional con partition-lanes. 3) La vista resuelta es sldb.api.notations.resolve_view (src/sldb/api/notations/resolve_view.py, la que usa sldb notations validate y graph_ui). Comprobar con un test que trae layout.kind y layout.by tal cual; si los pierde, pasarlos ahí. 4) Tests en un archivo nuevo tests/notations/test_layout_partition_lanes.py, construyendo la NotationDoc y la spec con los mismos helpers o fixtures que usa tests/notations/test_notation_view_and_routes.py: partition-lanes con by válido; partition-lanes sin by válido; by con kind graph rechazado; by '   ' rechazado; la vista resuelta de una spec con esa notación conserva kind y by. 5) Commit con mensaje 'feat: layout partition-lanes con by en NotationDoc', sin trailer Task-Id. Correr pytest -q tests/notations/test_layout_partition_lanes.py tests/notations/test_notation_models_and_builtins.py tests/notations/test_notations_validate_cli.py; la suite completa la corre el host.

## Validation

_List the checks required before this task can close._

- pytest -q tests/notations/test_layout_partition_lanes.py tests/notations/test_notation_models_and_builtins.py tests/notations/test_notations_validate_cli.py

## Done When

_Name the observable condition that makes the task complete._

sldb notations validate acepta una NotationDoc con layout {kind: partition-lanes, by: lane} y la vista resuelta de una spec con esa notación trae layout.kind == 'partition-lanes' y layout.by == 'lane'; los tests nuevos de tests/notations/ pasan.

---
sldb:
  by: agent
  at: '2026-11-17T02:07:51Z'
  authority: generated
  via: create_document
id: task-sldb-api-expone-render-con-roundtrip-renderizar-el-payload-de-un-modelo-a-markdown-y-validar-que-vue
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-222854-suggestion-pedido-render-roundtrip-de-modelo-p-blico-en-sldb-api-graph-ui-usa-sldb-runtime-validation.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/document_render.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.api expone render con roundtrip: renderizar el payload de un modelo a Markdown y validar que vuelve igual antes de escribir

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui importa render_model_markdown y validate_model_input_roundtrip de sldb.runtime.validation para renderizar un payload y comprobar el roundtrip antes de escribir; sldb.api no tiene equivalente público (render_document_markdown y render_model_template no validan el roundtrip). Origen: desk/inbox/20261116-222854-suggestion-pedido-render-roundtrip-de-modelo-p-blico-en-sldb-api-graph-ui-usa-sldb-runtime-validation.md.

## Goal

_Describe the concrete result this task must produce._

Una función pública de sldb.api.documents recibe un modelo (registrado, por nombre, o la clase) y un payload, devuelve el Markdown renderizado y el resultado del roundtrip (ok y diferencias), sin escribir nada; graph_ui puede dejar de importar sldb.runtime.validation.

## Scope

_State what is in scope and what is out of scope._

Entra: la función en src/sldb/api/documents/document_render.py (o un módulo nuevo del mismo paquete), exportada en el __all__ de sldb.api.documents, reutilizando render_model_markdown y validate_model_input_roundtrip; docstring con el contrato; tests en tests/api/test_api_documents.py (payload válido da ok; payload que no vuelve igual da las diferencias). CHANGELOG. No entra: cambiar render_document_markdown.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/runtime/validation.py y document_render.py. 2) Implementar y exportar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; la función se importa desde sldb.api.documents; CHANGELOG y commit; aviso a graph_ui.

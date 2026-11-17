---
sldb:
  by: agent
  at: '2026-11-17T02:57:36Z'
  authority: generated
  via: create_document
id: task-sw4a-sldb-serve-expone-escribir-un-anclaje-y-leer-su-estado-y-la-cobertura-por-fuente-sobre-la-api-p
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-233813-suggestion-sw4-flujo-3-6-4-anclar-de-verdad-hoy-crear-atomdoc-y-anclar-no-guarda-un-anclaje-y-el-estado-del-anclaje-se-calcula-en-la-ui.md
depends_on: []
pills: []
files:
- src/sldb/api/anchors/__init__.py
- src/sldb/cli/serve/http_server.py
- tests/test_serve.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW4a: sldb serve expone escribir un anclaje y leer su estado y la cobertura por fuente, sobre la API pública de anclas

## Rationale

_Explain why this task exists or the business driver behind it._

surface crea átomos sin guardar el anclaje y recalcula su estado con indexOf; sldb ya tiene write_anchor (src/sldb/api/anchors/anchor_docs.py) y anchor_state (src/sldb/store/edge_index/doc_anchor_states.py), pero sldb serve no tiene ninguna ruta de anclaje. Los consumidores no reimplementan sldb. Primera de dos tareas (luego SW4b en surface). Origen: desk/inbox/20261116-233813-suggestion-sw4-flujo-3-6-4-anclar-de-verdad-hoy-crear-atomdoc-y-anclar-no-guarda-un-anclaje-y-el-estado-del-anclaje-se-calcula-en-la-ui.md.

## Goal

_Describe the concrete result this task must produce._

sldb serve tiene rutas para escribir un anclaje (con offsets o cita), leer el estado de los anclajes de un documento (intact, changed, lost, reconnected) y la cobertura de anclajes por fuente, todas sobre la API pública de sldb.api.anchors, con la misma autenticación y forma de error que el resto de rutas.

## Scope

_State what is in scope and what is out of scope._

Entra: un módulo nuevo de rutas de anclaje en el paquete sldb.cli.serve registrado como los demás *_routes.py; si falta una función pública para la cobertura por fuente, agregarla en sldb.api.anchors; tests en tests/test_serve.py (escribir un anclaje, leerlo intact, editar la fuente y leerlo changed, cobertura). CHANGELOG y la doc de rutas de serve. No entra: surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer anchor_docs.py, doc_anchor_states.py, src/sldb/cli/serve/http_server.py y un *_routes.py de escritura. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit.

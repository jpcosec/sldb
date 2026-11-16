---
sldb:
  by: agent
  at: '2026-11-16T13:08:17Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-carga-tolerante-edge-index-py-y-runtime-documents-py-con-una-clase-cada-uno-y-query
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/edge_index/edge_index.py
- src/sldb/api/documents/runtime_documents.py
- src/sldb/store/query.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los
---

# Clean code tras carga-tolerante: edge_index.py y runtime_documents.py con una clase cada uno y query.py bajo 80 líneas

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: src/sldb/store/edge_index/edge_index.py y src/sldb/api/documents/runtime_documents.py tienen 2 clases (máximo 1) y src/sldb/store/query.py tiene 81 líneas efectivas (máximo 80). Lo introdujo task-carga-tolerante (163726f2); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-carga-tolerante, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Mover EdgeProblem (y edge_problem, ENDPOINT_NOT_A_NODE) a un módulo nuevo edge_problem.py del paquete sldb.store.edge_index; mover InvalidDocument a un módulo nuevo invalid_document.py del paquete sldb.api.documents, reexportando desde el módulo original; bajar query.py a 80 líneas extrayendo un helper de la carga con rechazados a un módulo vecino. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_doc_invalid_check.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Todos los comandos de Validation pasan (incluidos test_clean_code_rules y check.sh --fast); git diff no toca archivos de tests de comportamiento; CHANGELOG y commit.

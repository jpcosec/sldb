FILE:desk/tasks/task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse.md
---
sldb:
  by: agent
  at: '2026-11-17T02:47:46Z'
  authority: generated
  via: create_document
id: task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/provenance.md
depends_on: []
pills: []
files:
- src/sldb/api/anchors/anchor_docs.py
- tests/api/test_provenance.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El parámetro actor de la API de escritura se respeta en lugar de aceptarse e ignorarse

## Rationale

_Explain why this task exists or the business driver behind it._

Varias funciones de sldb.api aceptan actor y lo ignoran: unas 15 tienen actor: str | None = None, y algunas lo pisan (por ejemplo src/sldb/api/anchors/anchor_docs.py:47 llama save_document_payload con actor=None). Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Toda función pública de escritura que acepta actor lo pasa hasta donde se registra la procedencia (sello sldb.by del documento), de modo que un documento escrito con actor=X queda firmado por X; ninguna lo descarta.

## Scope

_State what is in scope and what is out of scope._

Entra: inventario de las funciones con parámetro actor; ver cómo se forma el sello de procedencia (docs/architecture/provenance.md y el código que lo escribe); pasar actor hasta ahí en cada camino, incluido anchor_docs.write_anchor; tests en tests/api/test_provenance.py. Si alguna no puede respetarlo, se documenta en su docstring y en result-summary.md. CHANGELOG. No entra: cambiar el formato del sello.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de 'actor' en src/sldb/api. 2) Seguir el camino hasta el sello. 3) Corregir cada función. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_provenance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; ninguna función pública de escritura descarta actor; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-parámetro-actor-de-la-api-de-escritura-se-respeta-en-lugar-de-aceptarse-e-ignorarse: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


FILE:desk/tasks/task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene.md
---
sldb:
  by: agent
  at: '2026-11-17T02:45:31Z'
  authority: generated
  via: create_document
id: task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/user-manual.md
depends_on: []
pills: []
files:
- docs/user-manual.md
- tests/test_serve.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La documentación de sldb serve nombra todas sus rutas HTTP, con un chequeo que lo mantiene

## Rationale

_Explain why this task exists or the business driver behind it._

El documento que describe sldb serve nombra 5 de unas 45 rutas que define src/sldb/cli/serve/ (docs_routes, graph_routes, models_routes, etc.). Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

Un documento de sldb lista cada ruta de sldb serve (método, path, parámetros y qué devuelve en una línea), y un test falla si una ruta del código no está en el documento o viceversa.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar el documento actual de serve (docs/user-manual.md u otro de docs/ que lo describa), completarlo con todas las rutas registradas en src/sldb/cli/serve/, y un test en tests/test_serve.py que compare las rutas registradas con las del documento. CHANGELOG. No entra: cambiar rutas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver cómo se registran las rutas en src/sldb/cli/serve/http_server.py y los *_routes.py. 2) Completar el documento. 3) Test. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con el test nuevo; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


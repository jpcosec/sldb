FILE:desk/tasks/task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a.md
---
sldb:
  by: agent
  at: '2026-11-17T02:44:41Z'
  authority: generated
  via: create_document
id: task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/current-cli-tree.md
depends_on: []
pills: []
files:
- docs/architecture/current-cli-tree.md
- src/sldb/cli/commands/selfdoc.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La doc del árbol del CLI cubre todos los subcomandos y grupos, y selfdoc check detecta cuando falta alguno

## Rationale

_Explain why this task exists or the business driver behind it._

docs/architecture/current-cli-tree.md omite unos 45 subcomandos y 11 grupos del CLI real, y sldb selfdoc check no lo detecta. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

current-cli-tree.md lista todos los grupos y subcomandos que define el parser de sldb, y selfdoc check falla nombrando cada grupo o subcomando del parser que la doc no menciona (y cada uno que la doc nombra y ya no existe).

## Scope

_State what is in scope and what is out of scope._

Entra: (1) un chequeo en selfdoc que recorre el árbol de argparse de sldb y lo compara con los comandos nombrados en current-cli-tree.md, con hallazgos accionables; (2) completar current-cli-tree.md (si es generable desde el parser, generarlo y que el chequeo compare con lo generado); (3) tests en tests/selfdoc/. CHANGELOG. No entra: reescribir las descripciones de cada comando más allá de una línea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/commands/selfdoc.py, current-cli-tree.md y cómo se arma el parser (src/sldb/cli/parsers/). 2) Implementar el chequeo y completar la doc. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_parser.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python -m sldb selfdoc check
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; borrar una línea de current-cli-tree.md hace fallar selfdoc check nombrando el comando; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-doc-del-árbol-del-cli-cubre-todos-los-subcomandos-y-grupos-y-selfdoc-check-detecta-cuando-falta-a: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


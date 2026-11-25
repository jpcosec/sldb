FILE:desk/tasks/task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com.md
---
sldb:
  by: agent
  at: '2026-11-17T14:48:10Z'
  authority: generated
  via: save_document_payload
id: task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md
depends_on: []
pills: []
files:
- src/sldb/cli/commands/links.py
- tests/test_links.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El scan de enlaces ignora el contenido de los bloques de código (fenced e inline) y no los informa como enlaces rotos

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, el scan de enlaces de un documento real lista dos veces 'target' como enlace roto, y los dos vienen de ejemplos dentro de bloques de código del Markdown. Origen: desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md.

## Goal

_Describe the concrete result this task must produce._

El scan de enlaces de sldb (comando sldb links y la API que usa) no cuenta como enlace nada que esté dentro de un bloque de código cercado ni de un código en línea; los enlaces reales se siguen detectando igual.

## Scope

_State what is in scope and what is out of scope._

Entra: encontrar el parser de enlaces que usa src/sldb/cli/commands/links.py y excluir los bloques de código cercados (con backticks o tildes) y el código en línea; tests en tests/test_links.py con un documento que tiene enlaces reales y ejemplos dentro de bloques de código. CHANGELOG. No entra: otros tipos de referencia.

Precisiones (coordinador, corrección 2, 2026-11-17): un fence puede abrirse en la misma línea que el marcador de un ítem de lista ("- ```", "1. ```python", "* ~~~"); su apertura se mide en la columna de contenido del ítem y su cierre puede venir indentado a esa columna. Un cierre indentado sin apertura vista no abre un bloque nuevo que se trague el resto del archivo. Tests: los cuatro casos de runs/subagents/20261116-test-lk-c1/result-summary.md (dos con enlaces reales después del bloque y dos con [[...]] dentro del bloque), cada uno contrastado con markdown-it-py commonmark si está instalado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer links.py y el parser que llama. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a sldb-ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


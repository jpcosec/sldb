---
sldb:
  by: agent
  at: '2026-11-17T13:13:11Z'
  authority: generated
  via: create_document
id: task-baja-prioridad-canonizar-los-nombres-de-llamada-ts-js-cuya-cadena-empieza-en-un-array-binario-new-o
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
- priority:low
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
---

# Baja prioridad: canonizar los nombres de llamada TS/JS cuya cadena empieza en un array, binario, new o literal (hoy canonical: false)

## Rationale

_Explain why this task exists or the business driver behind it._

C3 TS se cerró emitiendo con canonical: false los nombres de llamada cuyo objeto inicial es un array, una expresión binaria, un new o un literal (unos 123 de 2000 en tres frontends reales), con el texto de la expresión. Decisión del supervisor (2026-11-17): canonizarlos más adelante, con baja prioridad.

## Goal

_Describe the concrete result this task must produce._

Los nombres de llamada que hoy salen con canonical: false tienen una forma canónica definida y documentada (por ejemplo marcadores fijos [...] para arrays, (expr) para binarios, Clase() para new y (lit) para literales) y salen con canonical: true y en la relación calls si nombran un símbolo.

## Scope

_State what is in scope and what is out of scope._

Entra: definir la forma para cada tipo de expresión inicial, implementarla en el armado del nombre de llamada de sldb.code para TS/JS, actualizar el docstring y los tests en tests/selfdoc/test_treesitter_symbols.py, y medir sobre los tres frontends reales del workspace cuántos quedan no canónicos. CHANGELOG. No entra: Python.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de los no canónicos en los tres frontends. 2) Definir la forma. 3) Implementar. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; el número de nombres no canónicos en los tres frontends baja y los que quedan están documentados; CHANGELOG y commit.

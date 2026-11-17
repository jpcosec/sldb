---
sldb:
  by: agent
  at: '2026-11-17T02:46:15Z'
  authority: generated
  via: create_document
id: task-el-tercer-valor-del-lenguaje-de-predicados-incomplete-se-demuestra-alcanzable-con-un-test-sobre-dato
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- docs/architecture/rules-language.md
depends_on: []
pills: []
files:
- src/sldb/api/where.py
- docs/architecture/rules-language.md
- tests/test_predicates_cli.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El tercer valor del lenguaje de predicados (incomplete) se demuestra alcanzable con un test sobre datos reales o se retira

## Rationale

_Explain why this task exists or the business driver behind it._

El lenguaje de predicados tiene tres valores (true, false, incomplete), pero incomplete parece inalcanzable con datos reales: ningún camino de evaluación sobre un store real lo produce. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16). Código: src/sldb/api/where.py, src/sldb/store/graph/language/predicate_explain.py, predicate_reach.py y src/sldb/api/rules/.

## Goal

_Describe the concrete result this task must produce._

O hay un test que, con un store real armado en tmp_path, obtiene incomplete de una evaluación pública (where o rules check) y documenta cuándo ocurre; o incomplete se retira del lenguaje, de la API y de la doc sin cambiar los resultados true/false existentes.

## Scope

_State what is in scope and what is out of scope._

Entra: buscar todos los productores y consumidores de incomplete; intentar construir el caso real; decidir con evidencia en result-summary.md; implementar la opción elegida con tests en tests/test_predicates_cli.py o tests/api/test_rules_evaluation.py; actualizar docs/architecture/rules-language.md. CHANGELOG. No entra: otros cambios del lenguaje.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de incomplete en src/sldb. 2) Intentar el caso real. 3) Decidir y documentar la decisión. 4) Implementar y testear. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_predicates_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md explica la decisión con evidencia; CHANGELOG y commit.

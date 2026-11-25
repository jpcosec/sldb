FILE:desk/tasks/task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar.md
---
sldb:
  by: agent
  at: '2026-11-17T01:44:27Z'
  authority: generated
  via: create_document
id: task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-214137-suggestion-stores-check-errores-rules-builtin-tag-namespace-domain-llegan-con-fix-vac-o.md
depends_on: []
pills: []
files:
- src/sldb/api/rules/builtin_tag_findings.py
- tests/api/test_rules_evaluation.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La regla builtin tag_namespace:domain sugiere un fix concreto en stores check (qué namespace declarar o qué tag cambiar)

## Rationale

_Explain why this task exists or the business driver behind it._

En el store de sldb-ui, stores check --format json devuelve 5 errores rules/builtin:tag_namespace:domain con fix vacío, y la UI solo puede decir que el CLI no sugirió nada. Origen: desk/inbox/20261116-214137-suggestion-stores-check-errores-rules-builtin-tag-namespace-domain-llegan-con-fix-vac-o.md.

## Goal

_Describe the concrete result this task must produce._

Cada hallazgo de la regla builtin tag_namespace:domain trae en fix un texto accionable: el namespace a declarar en la política del store (con el comando o la clave exacta) o los tags válidos de ese namespace.

## Scope

_State what is in scope and what is out of scope._

Entra: el texto de fix en src/sldb/api/rules/builtin_tag_findings.py (y builtin_tag_rules.py si hace falta) para esa regla, nombrando el namespace y la acción; revisar las demás reglas builtin de tags y llenar su fix si también está vacío; tests en tests/api/test_rules_evaluation.py. CHANGELOG. No entra: cambiar qué detecta la regla.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer builtin_tag_rules.py y builtin_tag_findings.py. 2) Llenar fix. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rules_evaluation.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_tags.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; ningún hallazgo builtin de tags sale con fix vacío; CHANGELOG y commit; aviso a sldb-ui.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-regla-builtin-tag-namespace-domain-sugiere-un-fix-concreto-en-stores-check-qué-namespace-declarar: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


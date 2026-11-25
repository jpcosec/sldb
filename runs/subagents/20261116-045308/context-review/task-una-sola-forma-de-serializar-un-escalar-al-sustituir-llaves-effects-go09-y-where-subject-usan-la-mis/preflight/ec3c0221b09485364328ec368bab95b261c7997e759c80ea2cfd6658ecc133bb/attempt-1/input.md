FILE:desk/tasks/task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis.md
---
sldb:
  by: agent
  at: '2026-11-16T04:13:59Z'
  authority: generated
  via: create_document
id: task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/query_engine/where_literal.py
- src/sldb/store/query_engine/where_subject.py
- src/sldb/api/edges/edge_effects.py
- tests/store/test_predicate_language.py
- tests/api/test_edge_effects.py
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-evaluates-declared-rules-consumers-author-them
from_drawer: desk/drawer/tasks/task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md
---

# Una sola forma de serializar un escalar al sustituir llaves: effects (GO09) y where_subject usan la misma función

## Rationale

_Explain why this task exists or the business driver behind it._

La sustitución {campo} tiene dos serializadores: src/sldb/api/edges/edge_effects.py:38-44 (_written) usa yaml.safe_dump (1e20 da 1.0e+20, booleanos true/false, y hoy una fecha lanza LookupError), mientras src/sldb/store/query_engine/where_literal.py:47-51 (scalar_literal, usado por fill_braces de src/sldb/store/query_engine/where_subject.py:19) usa Decimal sin exponente y devuelve None para booleanos. El mismo valor sale distinto según dónde se sustituya. Hallazgo de GO09 (H3, H4). Origen: drawer desk/drawer/tasks/task-dos-formas-de-serializar-un-escalar-al-sustituir-llaves-effects-de-go09-y-where-subject.md.

## Goal

_Describe the concrete result this task must produce._

Existe una función brace_text(value) -> str en src/sldb/store/query_engine/where_literal.py que usan tanto edge_effects._written como fill_braces, con estas salidas exactas: int y Decimal sin exponente (1e20 -> 100000000000000000000), float con repr más corto sin exponente cuando sea posible (0.5 -> 0.5), bool -> true/false, datetime.date -> ISO 8601 (2026-11-16), str tal cual; cualquier otro tipo lanza TypeError con el tipo.

## Scope

_State what is in scope and what is out of scope._

Entra: escribir brace_text, cambiar _written y scalar_literal/fill_braces para usarla, y tests parametrizados con los cinco casos de Goal en tests/store/test_predicate_language.py y tests/api/test_edge_effects.py (mismo valor, mismo texto por los dos caminos). Si un test existente esperaba 1.0e+20 o None para bool, se actualiza al formato nuevo y el commit lo dice. CHANGELOG.md. No entra: cambiar la gramática del lenguaje de reglas ni los literales que el parser acepta.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer edge_effects.py 30-50, where_literal.py 40-60 y where_subject.py 1-40. 2) Escribir brace_text. 3) Usarla en los dos caminos. 4) Tests. 5) Correr los tres archivos de Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_edge_effects.py
- TMPDIR=/dev/shm pytest -q tests/store/test_predicate_language.py
- TMPDIR=/dev/shm pytest -q tests/store/test_where_empty_and_errors.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan; grep -n "safe_dump" src/sldb/api/edges/edge_effects.py ya no aparece en _written; los cinco casos dan el mismo texto por effects y por where_subject; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-una-sola-forma-de-serializar-un-escalar-al-sustituir-llaves-effects-go09-y-where-subject-usan-la-mis: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


---
sldb:
  by: agent
  at: '2026-11-16T06:18:43Z'
  authority: generated
  via: save_document_payload
id: task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-test-where-retired-de-go10-confunde-la-relación-contains-con-el-operador-viejo.md
depends_on: []
pills: []
files:
- tests/store/test_where_retired.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# test_where_retired distingue el operador viejo contains de la relación de aristas contains

## Rationale

_Explain why this task exists or the business driver behind it._

tests/store/test_where_retired.py::test_no_old_operator_in_the_code_of_docs (aceptación de GO10, 1e6ecd55) busca los ocho operadores viejos del lenguaje de consultas (eq, ne, gt, lt, contains, starts_with, is_null, is_not_null) como palabra entera en todo bloque o span de código de docs/. Pero contains también es el nombre de la relación de aristas de contención (__containment__, sldb edges). Un doc que nombra esa relación entre comillas invertidas hace fallar la suite aunque no hable del lenguaje viejo; pasó con tres docs y se tapó en c2d279d0 quitando las comillas. Origen: nota del inbox desk/inbox/inbox-note-test-where-retired-de-go10-confunde-la-relación-contains-con-el-operador-viejo.md.

## Goal

_Describe the concrete result this task must produce._

El test sigue fallando cuando un bloque o span de código de docs/ usa un operador viejo como operador de predicado, y deja de fallar cuando contains aparece solo como nombre de la relación de aristas.

## Scope

_State what is in scope and what is out of scope._

Entra: cambiar tests/store/test_where_retired.py y agregar una línea en CHANGELOG.md bajo el encabezado de la versión sin publicar ("test_where_retired ya no confunde la relación contains con el operador viejo"). Regla exacta: los siete operadores eq, ne, gt, lt, starts_with, is_null, is_not_null se siguen contando como hoy (palabra entera en código de docs/). contains se cuenta como operador viejo solo si casa el patrón PREDICATE_CONTAINS = re.compile(r"(?<![\w.])[A-Za-z_][\w.]*\s+contains\s+(\"|\x27|\d|\[|[A-Za-z_])|(?<!\w)contains\s*:"), es decir: un identificador de campo (letras, dígitos, guion bajo y puntos, como status o a.b) seguido de espacios, contains, espacios y el inicio de un valor (comilla, dígito, corchete o identificador), o la forma contains: (clave de un mapeo de operadores). contains solo, entre comillas invertidas o como argumento de una opción (--relation contains) no cuenta. Dos tests nuevos en el mismo archivo, sobre texto en memoria: test_contains_as_edge_relation_is_not_an_old_operator (los textos "contains", "sldb edges --relation contains" y "la relación contains" dan cero operadores) y test_contains_as_predicate_is_an_old_operator ("status contains \"x\"" y "contains: foo" dan contains). Si docs/ actual ya tiene otro operador viejo y el test falla por eso, no se toca docs/: se reporta el archivo y la línea en el informe del ejecutor y la tarea queda bloqueada. No entra: tocar docs/ ni src/, cambiar la excepción de la tabla Histórico de docs/architecture/rules-language.md, ni cambiar el test de identificadores where_parse/FieldCondition.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/store/test_where_retired.py completo (OPERATORS en la línea 18, INLINE, _code, _historic_rows y test_no_old_operator_in_the_code_of_docs). 2) Quitar contains de OPERATORS y agregar la constante PREDICATE_CONTAINS con el regex exacto de Scope. 3) Agregar la función pura _old_operators(code: str) -> list[str] que devuelve los operadores viejos encontrados en un fragmento de código (los de OPERATORS más "contains" cuando casa PREDICATE_CONTAINS), y hacer que test_no_old_operator_in_the_code_of_docs la use. 4) Agregar los dos tests nuevos, que llaman a _old_operators directamente. 5) Correr el archivo. 6) Línea en CHANGELOG.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py

## Done When

_Name the observable condition that makes the task complete._

TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py pasa con los dos tests nuevos; _old_operators("sldb edges --relation contains") == [] y _old_operators("status contains \"x\"") == ["contains"]; git diff --stat del commit muestra solo tests/store/test_where_retired.py y CHANGELOG.md.

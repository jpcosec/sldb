FILE:desk/tasks/task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains.md
---
sldb:
  by: agent
  at: '2026-11-16T03:42:27Z'
  authority: generated
  via: create_document
id: task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-test-where-retired-de-go10-confunde-la-relación-contains-con-el-operador-viejo.md
depends_on: []
pills: []
files:
- tests/store/test_where_retired.py
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

Entra: cambiar solo tests/store/test_where_retired.py. El regex OPERATORS (línea 18) deja de casar contains suelto; contains cuenta como operador viejo solo en contexto de predicado: precedido por un nombre de campo y seguido de un valor (forma `campo contains valor`) o en la forma `contains:` / `op: contains`. Los otros siete operadores no cambian. Se agregan dos tests nuevos en el mismo archivo que llaman a las funciones auxiliares del test sobre texto en memoria: uno donde `contains` aparece como relación (por ejemplo `sldb edges --relation contains` o `` `contains` `` solo) y no se cuenta, y otro donde `status contains "x"` sí se cuenta. No entra: tocar docs/ ni src/, cambiar la excepción de la tabla Histórico de docs/architecture/rules-language.md, ni cambiar el test de identificadores where_parse/FieldCondition.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer tests/store/test_where_retired.py completo (OPERATORS en la línea 18, _code, _historic_rows y el test test_no_old_operator_in_the_code_of_docs). 2) Separar contains de OPERATORS en un patrón aparte que exija contexto de predicado, por ejemplo r"\w+\s+contains\s+\S" o r"(?<!\w)contains\s*:" ; el resto de operadores sigue con el regex actual. 3) Factorizar la detección en una función pura (por ejemplo _old_operators(code: str) -> list[str]) para poder probarla sin archivos. 4) Agregar test_contains_as_edge_relation_is_not_an_old_operator y test_contains_as_predicate_is_an_old_operator. 5) Correr el archivo y confirmar que pasa sobre docs/ actual.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py

## Done When

_Name the observable condition that makes the task complete._

TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py pasa con los dos tests nuevos incluidos; el test de relación falla si se vuelve al regex viejo (comprobado revirtiendo el patrón localmente) y el de predicado pasa con el patrón nuevo; el commit toca solo ese archivo y CHANGELOG.md.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-test-where-retired-distingue-el-operador-viejo-contains-de-la-relación-de-aristas-contains: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


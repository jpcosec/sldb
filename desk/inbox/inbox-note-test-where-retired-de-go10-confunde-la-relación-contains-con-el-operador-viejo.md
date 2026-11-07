---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-06T21:02:37-03:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# test_where_retired de GO10 confunde la relación contains con el operador viejo

_Describe the incoming message with enough evidence to triage._

tests/store/test_where_retired.py::test_no_old_operator_in_the_code_of_docs (aceptación de GO10, 1e6ecd55) busca los ocho operadores viejos (eq, ne, gt, lt, contains, starts_with, is_null, is_not_null) como palabra entera en todo bloque o span de código de docs/. contains es además el nombre de la relación de aristas de contención (__containment__, sldb edges), así que un doc que la nombra entre comillas invertidas falla aunque no hable del lenguaje viejo. Pasó en la suite completa sobre 2d5cf98e con bootstrap-model-set.md (B2), references.md (GD22) y views.md (GD25); se arregló en c2d279d0 sacando las comillas, pero el test va a seguir dando falsos positivos. Propuesta: que el test distinga el operador, por ejemplo exigiendo contexto de predicado (un campo antes, o la forma op: valor) o admitiendo contains cuando va como relación de aristas, con un caso de test de cada lado. Coordinador de proyecto SLDB_1, 2026-11-06.

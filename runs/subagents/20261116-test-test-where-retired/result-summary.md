# Tester deskops-t-e73d2fad915b — task-test-where-retired

Veredicto global: **PASA**. Salida completa en `validation.log`; el script del tester está en `/dev/shm/tester_where_retired.py`, carga el módulo del test por ruta y no edita el repo.

| # | Punto | Veredicto | Evidencia |
|---|-------|-----------|-----------|
| 1 | Contrato leído | PASA | `deskops show task` solo muestra la cabecera, así que leí el scope, la validación y done_when en `desk/tasks/task-test-where-retired-….md`. |
| 2 | Diff sin commitear | PASA | `git diff --stat -- tests/store/test_where_retired.py CHANGELOG.md`: 2 archivos, +26/−4. En CHANGELOG hay una línea, bajo `## 0.1.13 — not released yet`. |
| 3 | Validación | PASA | `uvx --from "pytest>=8" pytest -q tests/store/test_where_retired.py`: `4 passed`, rc=0. Pasan los dos tests nuevos. |
| 4a | `_old_operators("sldb edges --relation contains") == []` | PASA | Lo comprueba el script del tester. |
| 4b | `_old_operators('status contains "x"') == ["contains"]` | PASA | Lo comprueba el script del tester. |
| 4c | El diff solo toca esos dos archivos | PASA, con una nota | El diff de la tarea toca solo `tests/store/test_where_retired.py` y `CHANGELOG.md`. Nada en `src/` ni en `docs/` es de esta tarea. El árbol tiene otros archivos modificados que no son de esta tarea (`apply_batch.py`, `lock.py`, `uv.lock`, `.sldb/...`), así que el commit tiene que incluir solo esos dos archivos para que `git diff --stat` del commit cumpla done_when. |
| 5a | `PREDICATE_CONTAINS` igual al regex del scope | PASA | `m.PREDICATE_CONTAINS.pattern == SCOPE`: igualdad exacta de cadenas. |
| 5b | Los otros siete operadores cuentan como palabra entera | PASA | `eq`, `ne`, `gt`, `lt`, `starts_with`, `is_null` e `is_not_null` cuentan en `field <op> 3` y no cuentan dentro de otra palabra (`x<op>y`, `<op>_z`). `OPERATORS` coincide exactamente con el regex viejo sin `contains`. |
| 5c | Caso negativo: con el regex viejo, el test de la relación falla | PASA | Repuse en memoria el `OPERATORS` viejo, con `contains`. `test_contains_as_edge_relation_is_not_an_old_operator` falla con `AssertionError: contains`. |

Casos extra que también salieron bien: `a.b contains 3`, `tags contains [1]`, `x contains y` y `contains:` dan `["contains"]`; `` `contains` `` da `[]`; `status eq 'a'` da `["eq"]`.

# Ejecutor deskops-e-f61ad438e462 — task-test-where-retired

Resultado: **LISTO, validación rc=0** (4 passed).

## Cambios
- `tests/store/test_where_retired.py`
  - `OPERATORS`: se quita `contains`; quedan los siete (`eq|ne|gt|lt|starts_with|is_null|is_not_null`) como palabra entera, igual que antes.
  - Constante nueva `PREDICATE_CONTAINS` con el regex exacto de Scope.
  - Función pura nueva `_old_operators(code) -> list[str]`: los de `OPERATORS` más un `"contains"` por cada match de `PREDICATE_CONTAINS`.
  - `test_no_old_operator_in_the_code_of_docs` usa `_old_operators` (mismo recorrido, misma excepción Histórico, mismo formato de hit `path:n: op`).
  - Tests nuevos: `test_contains_as_edge_relation_is_not_an_old_operator` ("contains", "sldb edges --relation contains", "la relación contains" → `[]`) y `test_contains_as_predicate_is_an_old_operator` (`status contains "x"` y `contains: foo` → `["contains"]`).
  - Docstring del módulo: un párrafo que explica la regla de `contains`.
  - Sin cambios: `_historic_rows`, `_code`, `_files`, `test_no_old_identifier_in_src_or_docs`.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet`, que empieza con "test_where_retired ya no confunde la relación contains con el operador viejo".

## done_when
- `pytest -q tests/store/test_where_retired.py` pasa con los dos tests nuevos: 4 passed, rc=0 (ver `validation.log`).
- `_old_operators("sldb edges --relation contains") == []` y `_old_operators('status contains "x"') == ["contains"]`: lo comprueban el test y la línea `python3 -c` en `validation.log` (rc=0).
- `git diff --stat` de los archivos de la tarea: solo `tests/store/test_where_retired.py` (+25 −4) y `CHANGELOG.md` (+1). No toqué nada más; el commit lo hace el coordinador.
- docs/ actual no tiene ningún otro operador viejo: el test de docs pasa, así que no hay nada que reportar ni causa de bloqueo.

## Comandos (rc)
1. `TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py` → rc=127: `pytest` no está en PATH, y `.venv/bin` del repo no tiene paquetes (ni pytest ni sldb).
2. `TMPDIR=/dev/shm .venv/bin/pytest ...` → rc=127 (no existe).
3. `TMPDIR=/dev/shm uvx --from "pytest>=8" pytest -q tests/store/test_where_retired.py` → **rc=0**, 4 passed, 1 warning (`asyncio_default_fixture_loop_scope` desconocida porque el pytest aislado no tiene pytest-asyncio; no afecta).
4. `python3 -c` con los dos asserts de done_when → rc=0.

## Desvíos / dudas
- Corrí la validación con un pytest aislado de `uvx` en lugar de `uv run`/`uv sync`, para no sincronizar `.venv` ni tocar `uv.lock` (que tiene cambios ajenos). El archivo de test solo importa `re` y `pathlib`, y `tests/conftest.py` solo `os` y `pytest`, así que el resultado es el mismo. **Aviso para el coordinador:** `.venv` de este checkout está vacío (sin pytest), y quizá convenga repararlo aparte.

## REFORMULACION

Encargo ejecutable (no agregado): en `tests/store/test_where_retired.py`, sacar `contains` de `OPERATORS` y añadir `PREDICATE_CONTAINS` con el regex literal del Scope; crear `_old_operators(code: str) -> list[str]` que sume los siete operadores de palabra entera más `"contains"` cuando case el patrón; usarla en `test_no_old_operator_in_the_code_of_docs`; añadir `test_contains_as_edge_relation_is_not_an_old_operator` y `test_contains_as_predicate_is_an_old_operator`. Añadir una línea en `CHANGELOG.md` bajo la versión sin publicar. Prohibido tocar `docs/` y `src/`. Repo: SLDB_1. Límite: si `docs/` ya falla por otro operador viejo, no se corrige: se reporta archivo/línea y se bloquea.

## AMBIGUEDADES

1. "bajo el encabezado de la versión sin publicar" — no cita versión ni formato; obligaría a inventar el número y el lugar exacto.
2. "se reporta el archivo y la línea en el informe del ejecutor y la tarea queda bloqueada" — no define formato del informe ni representación del bloqueo (`status: blocked`?); obligaría a inventar ambos.
3. "OPERATORS en la línea 18" — el número puede haber cambiado; obligaría a asumir que la línea 18 sigue siendo válida.
4. "git diff --stat del commit" — no aclara commit frente a árbol de trabajo; obligaría a elegir uno.

## DRY-RUN

Lecturas: `tests/store/test_where_retired.py` completo, `CHANGELOG.md` (encabezado), `docs/` solo en la ejecución del test. Cambios previstos: editar constantes, añadir `_old_operators`, ajustar test existente, dos tests nuevos, una línea de changelog. Dependencias: regex exacto del Scope; siete operadores intactos. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py`; comprobar `_old_operators("sldb edges --relation contains") == []` y `_old_operators("status contains \"x\"") == ["contains"]`; `git diff --stat` limitado a los dos archivos. Sin ejecutar nada.

## FUTURO

Un humano decide la versión del changelog y el formato del bloqueo si `docs/` falla; otro nodo aporta el informe del ejecutor.

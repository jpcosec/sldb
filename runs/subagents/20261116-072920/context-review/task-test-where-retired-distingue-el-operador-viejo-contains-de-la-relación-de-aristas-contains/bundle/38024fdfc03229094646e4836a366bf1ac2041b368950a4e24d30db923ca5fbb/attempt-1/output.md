## REFORMULACION

Propósito: eliminar el falso positivo de GO10 que confunde el operador viejo `contains` con la relación de aristas `contains`. Resultado: `tests/store/test_where_retired.py` distingue ambos casos y añade dos tests en memoria; una línea en `CHANGELOG.md`. Repo: SLDB_1. Archivos: `tests/store/test_where_retired.py` y `CHANGELOG.md`. Límites: no tocar `docs/` ni `src/`; no cambiar la excepción de la tabla Histórico ni el test de identificadores; si `docs/` ya tiene otro operador viejo que rompe el test, no tocarlo, reportar archivo y línea y bloquear la tarea.

## AMBIGUEDADES

1. Orden de retorno: cita «_old_operators(code: str) -> list[str] que devuelve los operadores viejos encontrados». No fija orden para múltiples hallazgos; obliga a inventar (¿aparición, orden de `OPERATORS`?).
2. Docstring del módulo: cita «the eight old operator names, as whole words». Tras el cambio ya no son ocho contados igual; no se indica actualizarlo. Obliga a decidir si se edita.
3. Encabezado del CHANGELOG: cita «bajo el encabezado de la versión sin publicar». No da el texto literal; obliga a inventarlo o buscarlo.
4. Informe del bloqueo: cita «se reporta el archivo y la línea en el informe del ejecutor». No define formato ni destino; obliga a inventar.
5. Goal frente a Scope: cita «usa un operador viejo como operador de predicado» frente a «los siete operadores … se siguen contando como hoy (palabra entera en código de docs/)». Tensión sobre si los siete exigen contexto de predicado.

## DRY-RUN

Nodo ejecutable (`task.code`), no agregado. Lecturas: `tests/store/test_where_retired.py` completo, `CHANGELOG.md`, y `docs/` solo si el test falla. Cambios previstos: quitar `contains` de `OPERATORS`; añadir `PREDICATE_CONTAINS` con el regex exacto; crear `_old_operators`; usarla en `test_no_old_operator_in_the_code_of_docs`; añadir los dos tests nuevos; línea en CHANGELOG. Dependencias: `re`, `pytest`, `TMPDIR=/dev/shm`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_where_retired.py`; casos `_old_operators("sldb edges --relation contains") == []` y `_old_operators("status contains \"x\"") == ["contains"]`; `git diff --stat` limitado a dos archivos. Todo hipotético, sin ejecutar.

## FUTURO

El ejecutor produce el commit y el informe de bloqueo si `docs/` falla; el ritual de testing valida y el de closeout cierra con `deskops closeout`. Un humano decide el destino de `docs/` si se bloquea.

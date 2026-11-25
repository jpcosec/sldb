## REFORMULACION

**Propósito:** corregir la regresión introducida por 6772820a —persistir el conjunto de documentos sucios en `.sldb_cache`— que rompe 16 tests de transacciones en `tests/api`.

**Resultado:** `tests/api` completo en verde conservando la persistencia del conjunto sucio y el modo incremental entre procesos (`tests/store/test_merkle_operation_cache.py` verde). Un rollback fallido debe dejar el conjunto persistido como antes de la transacción —incluido el caso ausente—, un hash de origen viejo debe seguir siendo conflicto y un fallo de rollback debe informar rutas no restauradas. No se cambian asserts de `tests/api`.

**Repo:** `SLDB_1/sldb`, worktree indicado por dispatch.

**Límites:** dentro, `documents_dirty.py`, `documents_dirty_persist.py`, código de transacciones/rollback y, opcionalmente, un test nuevo; fuera, modificar tests existentes de `tests/api`. Es un nodo ejecutable (`task.debug`), no un agregado.

## AMBIGUEDADES

1. «Fallan, entre otros, test_an_absent_dirty_set_stays_absent_after_a_failed_transaction...»: solo se nombran 4 de 16; obliga a inventar qué tests restantes cubren la regresión.
2. «tests/api completo da 16 failed sobre main local y 643 passed sobre origin/main»: no aclara cuál es la línea base verde esperada; obliga a inventar si se compara con `main` local u `origin/main`.
3. «y un test nuevo si hace falta»: no define criterio ni cobertura; obliga a inventar cuándo y qué probar.
4. «el código de transacciones/rollback de sldb que maneje el conjunto sucio»: no nombra módulos concretos; obliga a inventar la superficie exacta.
5. «La puerta 'identidad' de check.sh --fast en rojo por workbench_demo es la excepción autorizada»: `check.sh` no aparece en Validation; obliga a inventar si forma parte de la validación.
6. «desde el worktree que dispatch te da»: el input no incluye worktree ni rama; obliga a inventar su ubicación.

## DRY-RUN

**Lecturas:** TaskDoc, commit 6772820a y su padre, módulos de documentos sucios y transacciones/rollback, tests de `tests/api` citados.

**Cambios previstos:** hacer que el rollback restaure también el conjunto persistido, o persistir solo al confirmar; añadir test si se determina necesario.

**Dependencias:** worktree provisto por dispatch; autorización de la excepción de identidad (f055723d).

**Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api tests/store/test_merkle_operation_cache.py`; commit con trailer `Task-Id`.

## FUTURO

Dispatch entrega worktree y rama. Un humano confirma la excepción de identidad y decide la integración/cierre; otro nodo ejecuta la validación y el commit.

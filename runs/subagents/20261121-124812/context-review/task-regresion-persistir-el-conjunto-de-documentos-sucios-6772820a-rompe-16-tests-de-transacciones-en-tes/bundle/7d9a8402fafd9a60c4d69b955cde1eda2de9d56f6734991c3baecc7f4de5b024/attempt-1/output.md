## REFORMULACION
Propósito: corregir la regresión de 6772820a (persistir el conjunto sucio en `.sldb_cache`) que rompe tests de transacciones en `tests/api`. Resultado: `tests/api` en verde (0 fallas) con el conjunto sucio persistido y `tests/store/test_merkle_operation_cache.py` pasando, sin cambiar asserts existentes. Repo: sldb, en worktree provisto por dispatch. Límites: dentro `src/sldb/store/documents_dirty.py`, `documents_dirty_persist.py`, código de transacciones/rollback y un test nuevo si hace falta; fuera modificar tests de `tests/api`. Validación: comando pytest indicado.

## AMBIGUEDADES
1. «un test nuevo si hace falta»: no define criterio; obliga a inventar cuándo es necesario.
2. «haga que restaure también el persistido (o que la persistencia ocurra solo al confirmar la transacción)»: dos rutas alternativas sin criterio; obliga a inventar cuál elegir.
3. «el worktree que dispatch te da»: no identifica worktree ni dispatch; obliga a inventar ruta y mecanismo.
4. «La puerta 'identidad' ... por workbench_demo es la excepción autorizada (f055723d)»: no aporta `check.sh` ni el commit; obliga a inventar el alcance de la excepción.
5. «rompe 16 tests» convive con «9 failed sobre 6772820a» y «16 failed sobre main local»: no aclara qué conjunto exacto debe pasar a verde; obliga a inventar el universo de fallos.
6. La instrucción pide «las pills ligadas, los átomos ligados», pero el TaskDoc trae `pills: []` y `atoms: []`; obliga a inventar qué pills/átomos aplicar.
7. El ritual de testing dice «update or delete the ones that no longer describe the behavior», mientras el TaskDoc dice «No se cambian los asserts de los tests de tests/api»; obliga a inventar prevalencia.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout/phase y archivos nombrados (`documents_dirty.py`, `documents_dirty_persist.py`, código de transacciones/rollback, tests de `tests/api` y `test_merkle_operation_cache.py`). Cambios previstos: reproducir el comando del why y guardar salida; localizar la restauración del conjunto sucio en rollback; ajustar restauración o persistencia; añadir test solo si se decide; commit con trailer `Task-Id`. Dependencias: worktree de dispatch, commit 6772820a, excepción de puerta identidad, deskops para Board/closeout. Validaciones futuras: pytest indicado con `-n 4`, tests/store, `check.sh --fast`, `check_claims` si toca store y `closeout verify`.

## FUTURO
Dispatch entrega el worktree; un humano confirma la excepción f055723d; deskops actualiza el Board y ejecuta closeout; el ritual de fase captura aprendizaje y retira pills; el commit cierra la tarea.

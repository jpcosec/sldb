REFORMULACION
Propósito: corregir la transacción de sldb para que, en stores con RuleDoc y dirty set, el rollback restaure `.sldb_cache/rules/dirty.json` y relance el error original o `ConflictError`, no `RollbackError`. Resultado: cambios mínimos en `transaction_state.py`, `transaction_ops.py` y `transaction_paths.py` —y, si hace falta, `dirty_set.py` y `rules_on_write.py`—, un test de regresión en `tests/api/` y `CHANGELOG`. Repo: sldb `origin/main 758772c0`; consumidor de aceptación: deskops `wt/cc32 c9af867e`. Límites: no cambiar la semántica de `on_write` ni del dirty set; no tocar otros archivos de `.sldb_cache`, `replace_text` fuera de transacción ni el resto de la API.

AMBIGUEDADES
1. “lo mínimo para que la transacción snapshotee el dirty set”: no fija si se modifica `remember`, la apertura o ambos; obliga a elegir diseño.
2. “El worker elige la que menos toque y la explica”: “menos toque” no es un criterio medible; obliga a inventar la métrica.
3. “un test nuevo en tests/api/ (por ejemplo ... o un caso nuevo en ...)”: ubicación y nombre quedan abiertos; obliga a decidir.
4. “rules check o rules_on_check para crearlo”: no indica fixture, API ni estado inicial exacto; obliga a inventar el setup.
5. “lance un error propio”: no especifica clase ni mensaje; obliga a elegir una excepción.
6. “dirty.json quede byte a byte igual que antes”: no aclara el caso ausente en el test, aunque s1 pide borrarlo; obliga a inferir cobertura.

DRY-RUN
Lecturas: TaskDoc, `transaction_state.py`, `transaction_ops.py`, `transaction_paths.py`, `dirty_set.py`, `rules_on_write.py`, `tests/api/` y `CHANGELOG`. Cambios previstos: snapshotear `<rules_dir>/dirty.json` antes de la primera escritura, restaurarlo o borrarlo en rollback, preservar el error original; añadir tres casos de test y `CHANGELOG`. Dependencias: pytest, `TMPDIR=/dev/shm`, rama sldb y checkout deskops. Validaciones futuras: test nuevo, `test_transaction`, `test_rules_evaluation`, `test_write_paths_validate`, `test_replace_text` y `test_clean_code_rules`, de a uno; `wc -l`; `test_transaction` de deskops con `PYTHONPATH`.

FUTURO
El ejecutor concretará el punto de snapshot y la excepción de prueba. El coordinador o humano confirma la decisión revisable s1. Otro nodo o humano ejecutará la aceptación en deskops `wt/cc32` y decidirá el cierre.

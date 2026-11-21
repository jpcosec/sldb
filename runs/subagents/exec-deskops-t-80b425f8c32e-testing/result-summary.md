PASA

# Resultado — testing de la regresión del conjunto sucio persistido

Commit evaluado: `4b44a43af41c3634c78ac9a1ea106764450c9e34` — *Rollback restores the persisted dirty document set*
(`Task-Id: task-regresion-persistir-el-conjunto-de-documentos-sucios-6772820a-rompe-16-tests-de-transacciones-en-tes`).

## Archivos del ejecutor

- `src/sldb/api/documents/transaction_state.py`
- `src/sldb/store/documents_dirty.py`
- `src/sldb/store/documents_dirty_persist.py`

El commit no agrega archivos de test; no existen `tests/test_transaction_state.py` ni
`tests/test_documents_dirty*.py`. Se corrieron los tests de la superficie afectada y el test de
modo incremental que la tarea exige conservar.

## Tests (uno por archivo, TMPDIR=/tmp, venv del repo)

| Archivo | Resultado |
|---|---|
| `tests/api/test_transaction.py` | 16 passed |
| `tests/api/test_transaction_rules_dirty.py` | 4 passed |
| `tests/api/test_write_paths_validate.py` | 5 passed |
| `tests/store/test_merkle_operation_cache.py` | 9 passed |

Total: **34 passed, 0 failed** (los tres archivos de `tests/api` suman los 25 passed de la
reproducción del `why`).

Quedan verdes, entre otros, los casos que fallaban con `6772820a`:

- `test_an_absent_dirty_set_stays_absent_after_a_failed_transaction`
- `test_a_stale_source_hash_after_a_write_is_a_conflict_not_a_rollback_error`
- `test_a_failure_during_the_rollback_is_raised_with_the_unrestored_paths`
- `test_transaction_rejects_what_the_model_rejects_and_rolls_back`

No se modificaron los asserts de `tests/api`.

## Gates rápidos

`bash tools/check.sh --fast` (PATH con el venv del repo) termina rc=1 **únicamente** por la puerta
`identidad`:

```
ERROR directorio versionado sin clasificar en la raíz: workbench_demo
FAIL: identidad — ... 1 violaciones
```

Es la excepción autorizada por la tarea (`f055723d`) y es preexistente: el commit evaluado no toca
`workbench_demo` ni los contratos de identidad. Las demás puertas pasan:

- `núcleo aislado`: PASS
- `capas`: PASS (0 violaciones)
- `ejes`: PASS (0 violaciones)
- `superficie`: PASS (0 violaciones)

## Veredicto

**PASA**: el rollback restaura el conjunto sucio persistido, los tests de transacción afectados
vuelven a verde y el modo incremental entre procesos sigue pasando. La única puerta en rojo es la
excepción de identidad/`workbench_demo` autorizada expresamente.

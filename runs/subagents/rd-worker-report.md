# rd-worker: el rollback de la transacción restaura el dirty set de reglas

Rama `wt/rules-dirty-rollback` (base `4a5a33ad`). Commit del arreglo: `8491ddc4`. No hice push.
TaskDoc: `desk/tasks/task-transacción-el-rollback-restaura-el-dirty-set-de-reglas-sldb-cache-rules-dirty-json.md`.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/rd/`.

## Arreglo (b1)

`TransactionState.__init__` (`src/sldb/api/documents/transaction_state.py`), justo después de `store_signatures`, ahora llama a:

```python
self.remember([rules_dir(location.store_path) / f"{DIRTY}.json"])
```

- `snapshot` guarda los bytes del archivo, o `None` si no existe.
- `restore_all` lo reescribe, o lo borra si apareció durante la transacción.
- Como el archivo queda en `saved`, `unsnapshotted_drift` ya no lo cuenta como cambiado sin snapshot.
- `store_signatures` y `unsnapshotted_drift` no excluyen nada.
- `remember`, las operaciones, `dirty_set.py` y `rules_on_write.py` no cambian. La semántica de `mark_dirty` es la misma (s2).

`rules_dir` y `DIRTY` vienen de `sldb.api.rules.rule_cache`, que solo importa de `sldb.store`. No hay import circular: lo comprobé importando `sldb.api.documents.transaction_state`, `sldb.api.documents.transaction` y `sldb.api`. No hizo falta la alternativa de b1, la constante en `transaction_paths`.

## Aceptación

1. **Los 4 casos del test nuevo están verdes.** `tests/api/test_transaction_rules_dirty.py` reusa `World` y `world` de `tests/api/test_rules_evaluation.py` con el mismo import que ya usan otros tests de `tests/api`. El dirty set se crea con `api.rules_on_check`.
   - Sin el arreglo: `2 failed, 2 passed`. Los casos Boom y ConflictError salen con `RollbackError: Rollback incomplete; not restored: .sldb_cache/rules/dirty.json` (log `00-new-test-without-fix.log`).
   - Con el arreglo: `4 passed` (log `01-test_transaction_rules_dirty.log`).
   - Qué cubre cada caso:
     - **Boom:** sale `Boom`. Dentro del bloque `dirty.json` sí cambia, y después de la falla `dirty.json` y `x1.md` quedan byte a byte iguales.
     - **ConflictError:** una primera actualización ensucia el set; la segunda, con `expected_source_hash="stale"`, da `ConflictError`, y todo queda restaurado.
     - **Commit:** `dirty.json` cambia y contiene `X:x1`.
     - **Sin `dirty.json`:** sigue ausente después de la falla.
2. **De a uno, verdes.** Cada corrida se lanzó con `run.sh` y la guarda `pgrep` anclada.

   | archivo | resultado |
   |---|---|
   | tests/api/test_transaction_rules_dirty.py | 4 passed |
   | tests/api/test_transaction.py | 13 passed |
   | tests/api/test_rules_evaluation.py | 12 passed |
   | tests/api/test_write_paths_validate.py | 5 passed |
   | tests/api/test_replace_text.py | 16 passed |
   | tests/test_clean_code_rules.py | 949 passed |

3. **Prueba del consumidor:** deskops `c9af867e`, copia en `/dev/shm/deskops-cc32-rd`.
   - `sldb` importado: `/home/robocop/proyectos/SLDB_1/sldb-wt-rd/src/sldb/__init__.py`.
   - `tests/test_transaction.py`: `11 passed` (log `02-deskops-test_transaction.log`).
   - La copia se borró con `worktree remove --force`, y `deskops-wt-cc32` quedó limpio.
4. **wc -l**

   | archivo | antes | después |
   |---|---|---|
   | src/sldb/api/documents/transaction_state.py | 78 | 81 |
   | src/sldb/api/documents/transaction_ops.py | 93 | 93 |
   | src/sldb/api/documents/transaction_paths.py | 66 | 66 |
   | src/sldb/api/rules/dirty_set.py | 78 | 78 |
   | src/sldb/api/rules/rules_on_write.py | 49 | 49 |
   | CHANGELOG.md | 632 | 633 |
   | tests/api/test_transaction_rules_dirty.py | (nuevo) | 67 |

5. **CHANGELOG:** una entrada en `0.1.13 — not released yet`.

## Desvíos

- Ninguno en el código ni en el alcance: solo toqué `transaction_state.py`, el test nuevo, `CHANGELOG.md` y este informe.
- Mi primera espera de pytest usaba el patrón viejo, `pgrep -f "python -m pytest"`, y se quedó colgada porque se encontraba a sí misma. La corté y la relancé con el patrón anclado, como pidió coord2.

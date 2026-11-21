# Resultado
Causa: la transaccion no snapshoteaba .sldb_cache/documents_dirty.json; el rollback lo veia como deriva sin restaurar (RollbackError).
Cambio (commit 7276b2fb, rama deskops/deskops-e-4ea8e4d4dc22): TransactionState snapshotea el archivo persistido al entrar; tras forget_caches lo restaura de nuevo y llama a documents_dirty.reload (nuevo) para que la memoria lo relea. Archivos: src/sldb/api/documents/transaction_state.py, src/sldb/store/documents_dirty.py, src/sldb/store/documents_dirty_persist.py
Validacion: ver validation.log (tests/api + merkle_operation_cache: 652 passed; check.sh --fast solo rojo en identidad/workbench_demo, autorizado).
run_id: exec-deskops-e-4ea8e4d4dc22; session / session_sha256: no disponibles en este entorno.

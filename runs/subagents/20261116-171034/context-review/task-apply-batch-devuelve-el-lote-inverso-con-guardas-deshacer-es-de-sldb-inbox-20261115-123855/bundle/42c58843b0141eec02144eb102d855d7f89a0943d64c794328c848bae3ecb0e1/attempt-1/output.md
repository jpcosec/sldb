REFORMULACION
El nodo es una tarea de código ejecutable, no un agregado ni un paquete, en `/mnt/ssd/proyectos/SLDB_1`. Propósito: que deshacer sea responsabilidad de sldb, no de consumidores. Resultado: `BatchReport` con `inverse: list[dict]` aplicable mediante `apply_batch`; nuevo `batch_inverse.py` que captura el estado previo bajo lock antes de la transacción y arma el inverso después, aún bajo lock; `apply_batch` devuelve `BatchReport(saved, inverse)` con ≤10 líneas de lógica; pruebas en `tests/api/test_transaction.py`; CHANGELOG y commit. Límites: no implementar `undo_changes` del MCP, UI ni consumidores; no crecer `batch_prevalidate.py`; depende de que 022444 esté cerrada; solo los archivos listados.

AMBIGUEDADES
1. “Cada operación del inverso lleva expected_source_hash del estado que dejó el lote” frente a “delete -> create … el rechazo es el SLDBStoreError 'already exists'”. Un `create` inverso no admite `expected_source_hash`; obliga a inventar si se omite, se traduce o se añade una guarda nueva.
2. “un documento canónico (el render de su payload) vuelve byte a byte” frente a “la procedencia del front matter (sldb.by/at/via) puede cambiar y no cuenta para 'igual'”. Contradicción: obliga a decidir si “igual” compara bytes reales o payload renderizado sin procedencia.
3. “Decidir si se apoya en los snapshots que Transaction ya tiene para el rollback”. Decisión abierta sin criterio; obliga a inventar la arquitectura y su impacto.
4. “prevalidate_changes sigue siendo nombre de módulo en apply_batch.py”. En el archivo actual es una función importada, no un módulo; obliga a inventar si se refactoriza el import o solo se conserva el símbolo.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, la dependencia 022444, `apply_batch.py`, `batch_report.py`, `batch_prevalidate.py`, `transaction.py`, `store_lock`, tests de lock/escritura y CHANGELOG. Cambiaría `BatchReport`, añadiría `batch_inverse.py` con `before(...)` e `inverse(...)`, ajustaría `apply_batch` bajo el lock y añadiría los dos tests. Dependencias: snapshots de `Transaction`, payloads/hashes de prevalidación y cierre de 022444. Validaría con los comandos listados y `tools/check.sh --fast`; no se ejecuta nada aquí.

FUTURO
Otro nodo o humano debe cerrar 022444, decidir el uso de snapshots, implementar `undo_changes` en la tarea MCP, anotar el aviso a IR y ejecutar closeout/commit con deskops.

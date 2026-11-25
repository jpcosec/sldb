## REFORMULACION

Encargo en el repo sldb (cwd `/mnt/ssd/proyectos/SLDB_1`): hacer que `apply_batch` devuelva el lote inverso aplicable, porque deshacer es de sldb. Resultado: `BatchReport(saved, inverse)` con `inverse: list[dict]` en la forma que acepta `apply_batch`; deshacer = `apply_batch(report.inverse)`. Incluye módulo nuevo `batch_inverse.py` con `before(...)/inverse(...)` bajo el lock, wiring mínimo en `apply_batch.py` y dos tests en `tests/api/test_transaction.py` (ida y vuelta; rechazo sin escritura parcial). Límites: depende de la tarea 022444 cerrada; no expone la tool `undo_changes` del MCP (otra tarea); `batch_prevalidate.py` no crece; `apply_batch.py` ≤10 líneas de lógica.

## AMBIGUEDADES

1. «sin pasar de 10 líneas de lógica»: no define qué cuenta como línea ni como lógica; obliga a inventar el criterio de conteo.
2. «la procedencia del front matter (sldb.by/at/via) puede cambiar y no cuenta para "igual"»: no dice si `authority` u otros campos quedan excluidos; obliga a inventar la lista de campos ignorados.
3. «un documento canónico (el render de su payload)»: no especifica render ni normalización; obliga a inventar cómo se comparan bytes.
4. «track <-> untrack»: no indica payload, ruta ni `expected_source_hash`; obliga a inventar la forma del inverso.
5. «el rechazo es el SLDBStoreError "already exists" ... que se documenta como conflicto»: no aclara si se mapea a `ConflictError` o se propaga; obliga a inventar el contrato de error.
6. «tocar un documento entre medio»: no dice qué cambio ni qué documento; obliga a inventar el escenario del test.
7. «aviso a IR anotado en result-summary.md»: el archivo no figura en `files`; obliga a inventar ruta y formato.

## DRY-RUN

Un ejecutor futuro leería `apply_batch.py`, `batch_report.py`, `batch_prevalidate.py`, los modelos de `Transaction`, `tests/api/test_transaction.py`, `test_apply_batch_lock.py` y `CHANGELOG.md`. Cambios previstos: añadir `inverse` a `BatchReport`; crear `batch_inverse.py` con `before`/`inverse`; invocar `before` antes de la transacción e `inverse` después, aún bajo lock; devolver `BatchReport(saved, inverse)`; añadir los dos tests; actualizar CHANGELOG y `result-summary.md`. Dependencias: task 022444 cerrada, lock y snapshots de `Transaction`, API de prevalidación. Validaciones futuras: los seis pytest listados y `bash tools/check.sh --fast`.

## FUTURO

Cierre de la tarea 022444 (prerrequisito). Decisión del ejecutor sobre apoyarse o no en los snapshots de `Transaction` (pregunta abierta en la nota). Implementación de `undo_changes` en el MCP de sldb, aviso a IR, commit y CHANGELOG los resuelve otro nodo o un humano.

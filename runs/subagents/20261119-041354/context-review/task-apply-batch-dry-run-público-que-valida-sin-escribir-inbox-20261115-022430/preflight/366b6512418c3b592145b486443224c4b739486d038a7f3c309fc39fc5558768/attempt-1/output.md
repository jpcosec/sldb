## REFORMULACION
Propósito: en el repo `sldb`, hacer público `apply_batch(..., dry_run=True)` para que ejecute la prevalidación existente —forma, modelo, round-trip, guardas y destinos— bajo cerrojo y devuelva el informe o errores sin abrir transacción ni escribir. Resultado: API pública con `dry_run=False` por defecto, informe documentado y exportado, tests que prueban store byte a byte idéntico, mismo error para lote inválido, `apply_batches` sin cambios, posible integración con `propose_changes`, docs/CHANGELOG, gates y cierre de nota del inbox. Límites: no escribir en dry run, no cambiar `apply_batches`, respetar validaciones indicadas. Es tarea de código ejecutable, no agregado.

## AMBIGUEDADES
1. “devuelve el informe o los errores” frente a “levanta el mismo error”: no fija si los errores se devuelven o se excepcionan; obliga a elegir contrato.
2. “saved vacío y applied=False (o el campo que se agregue, documentado)”: no fija campos ni forma del `BatchReport`; obliga a inventar esquema.
3. “bajo el cerrojo”: no identifica qué cerrojo; obliga a asumir mecanismo de bloqueo.
4. “Exponer el modo en la API pública, documentar la forma del informe, exportarlo”: “exportarlo” no tiene antecedente inequívoco; obliga a decidir si exporta el flag, el informe o `prevalidate_changes`.
5. “Cerrar la nota del inbox al terminar”: no da ruta, ID ni operación de cierre; obliga a inventar el procedimiento.
6. “stores build --check”: no da comando exacto; obliga a asumir CLI y ruta.

## DRY-RUN
Lecturas hipotéticas: `apply_batch.py:27` y `:60`, `batch_prevalidate.py:22`, `batch_guards.py`, `api/__init__.py:13`, `mcp/write/tools.py:38`, tests de `api`/`mcp`, docs y CHANGELOG.
Cambios previstos: añadir `dry_run`; tras prevalidar bajo cerrojo, retornar antes de transacción; definir/exportar informe; tests de lote válido e inválido con comparación byte a byte; documentar; ajustar `propose_changes` solo si reimplementa prevalidación.
Dependencias: prevalidación, guardas, cerrojo, modelo de informe y API pública existentes.
Validaciones futuras: `pytest tests/api`, `pytest tests/mcp`, `bash tools/check.sh --fast`, `stores build --check` y comparación de stores. Sin ejecutar nada.

## FUTURO
Un humano u otro nodo decide el contrato exacto del informe y el cierre del inbox; el implementador decide p3 tras leer `propose_changes`; revisión acepta el resultado conjunto.

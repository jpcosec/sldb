## REFORMULACION

Nodo ejecutable (`task.code`, `ritual-execution`) del repo SLDB_1. Propósito: persistir en `documents_dirty.json`, dentro de `.sldb_cache`, el conjunto de documentos sucios, para que una corrida nueva lo lea y el modo incremental funcione entre procesos. Resultado: módulo nuevo `documents_dirty_persist.py`, `documents_dirty.py` ≤80 líneas, escritura atómica bajo `store_lock`, carga perezosa e invalidación por firma; archivo ausente o corrupto cae a cálculo completo sin error. Límites: no versionar el archivo ni cambiar qué se considera sucio.

## AMBIGUEDADES

1. «La firma es la de runtime_cache_signature.signature(s_path) (...) serializada»: no se define el formato de serialización ni cómo compararla. Obligaría a inventar representación JSON y criterio de igualdad.
2. «mark, clear e invalidate reescriben el archivo» frente a «bajo el lock del store»: no aclara si cada operación adquiere `store_lock`, ni si reescribe todo el archivo o solo las entradas de su modelo. Obligaría a inventar granularidad y política de bloqueo.
3. «Corrupto = no parsea como JSON o no tiene esas claves»: no cubre `entries` con forma inválida (no lista, elementos no triples, nombres no string). Obligaría a inventar qué cuenta como corrupción.
4. «tests en tests/store/test_merkle_operation_cache.py o un archivo de tests de store existente» frente a una Validación que solo ejecuta `test_merkle_operation_cache.py`: si se elige otro archivo, sus tests no se validarían. Obligaría a inventar o contradecir el alcance.
5. «documents_dirty.py no pase de 80 líneas»: no aclara si cuentan docstring e imports. Obligaría a inventar la métrica.

## DRY-RUN

Lecturas: `documents_dirty.py`, `user_cache.py` (ubicación de `.sldb_cache`), `runtime_cache_signature.py`, `io/__init__.py` (`store_lock`), consumidores de `names/mark/clear/invalidate` y tests existentes. Cambios previstos: crear `documents_dirty_persist.py` con carga/escritura JSON atómica (tmp + `os.replace`); conectar `documents_dirty.py` para hidratar `_DIRTY` en el primer `names()`, persistir en `mark/clear/invalidate` y borrar el archivo si es corrupto; añadir tests de proceso nuevo y corrupción; actualizar `CHANGELOG`. Dependencias: serialización de la firma y acceso al directorio de caché. Validaciones futuras: los cinco comandos del TaskDoc, empezando por `test_merkle_operation_cache.py`.

## FUTURO

Decisión humana u otro nodo: fijar el formato de firma, elegir el archivo de tests y confirmar si `mark/clear` toman lock. `deskops` ejecutará bind de pills y closeout/commit; los rituales de testing y closeout validarán y cerrarán.

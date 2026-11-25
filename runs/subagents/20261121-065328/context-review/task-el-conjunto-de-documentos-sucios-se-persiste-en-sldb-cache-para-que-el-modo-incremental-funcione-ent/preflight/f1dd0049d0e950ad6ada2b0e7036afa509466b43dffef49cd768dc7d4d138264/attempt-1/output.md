## REFORMULACION

Encargo ejecutable de código: persistir el conjunto de documentos sucios entre procesos. Resultado: `documents_dirty.json` en el directorio `.sldb_cache` del store (el que usa `src/sldb/store/user_cache.py`), con JSON `{"signature": <str>, "entries": [[modelo, namespace, [nombres...]], ...]}`; firma = `json.dumps(list(signature(s_path)), default=str)`, comparada por igualdad de cadena. Carga perezosa: la primera `names()` por store lee el archivo y llena `_DIRTY`; `mark`, `clear` e `invalidate` lo reescriben entero con escritura atómica (tmp + `os.replace`) bajo `store_lock` (`src/sldb/store/io/__init__.py`). Archivo corrupto (no parsea, faltan claves o `entries` con forma distinta de `[str, str, [str...]]`): se borra y `names()` devuelve `None`, sin log ni error. Lógica nueva en módulo nuevo `documents_dirty_persist.py` para que `documents_dirty.py` no pase de 80 líneas (medido por `tests/test_clean_code_rules.py`). Tests en `tests/store/test_merkle_operation_cache.py` con subprocess. Límites: no versionar el archivo ni cambiar qué se considera sucio. Cierre: los 5 comandos de Validation pasan + CHANGELOG + commit.

## AMBIGUEDADES

1. «la primera llamada a `names()` para un store lee el archivo una vez y llena `_DIRTY`»: no define cómo se distingue "por store" ni si `_DIRTY` se indexa por store; obligaría a inventar clave y estructura.
2. «mark, clear e invalidate reescriben el archivo»: no dice qué borra `clear` (¿una entrada, todo el store?) ni la firma de `mark`; obligaría a inventar API.
3. «`names()` devuelve None (cálculo completo)»: `names()` ya existe; obligaría a inventar si `None` es contrato nuevo y su compatibilidad con `test_edges_follow_the_contract.py`.
4. «invalidarlo cuando cambia la firma del store»: no especifica si al detectar firma distinta se descarta, borra o reescribe; obligaría a inventar comportamiento.
5. «se borra el archivo»: no indica si ocurre bajo `store_lock` ni si limpia `_DIRTY`; obligaría a inventar.
6. «el directorio `.sldb_cache` del store que ya usa `src/sldb/store/user_cache.py`»: no da función ni derivación exacta desde `s_path`; obligaría a inventar la ruta.
7. «CHANGELOG»: sin formato, versión ni texto; obligaría a inventar la entrada.

## DRY-RUN

Lecturas: `documents_dirty.py`, `user_cache.py`, `runtime_cache_signature.py`, `io/__init__.py`, consumidores de `names()`, `tests/store/test_merkle_operation_cache.py`, `tests/test_clean_code_rules.py`. Cambios previstos: nuevo `src/sldb/store/documents_dirty_persist.py`; edición mínima de `documents_dirty.py` (≤80 líneas) delegando carga/escritura; tests con subprocess (proceso nuevo ve dirty previo; archivo corrupto/forma inválida → `None`); CHANGELOG. Dependencias: `store_lock`, `signature(s_path)`, existencia/creación de `.sldb_cache`, `os.replace` en mismo filesystem. Validaciones futuras: los 5 comandos listados.

## FUTURO

El nodo de ejecución implementa y corre las validaciones; un humano decide el texto del commit/CHANGELOG y si basta la verificación parcial del análisis de origen (2026-11-16). CI (`tools/check.sh`) confirma el conjunto.

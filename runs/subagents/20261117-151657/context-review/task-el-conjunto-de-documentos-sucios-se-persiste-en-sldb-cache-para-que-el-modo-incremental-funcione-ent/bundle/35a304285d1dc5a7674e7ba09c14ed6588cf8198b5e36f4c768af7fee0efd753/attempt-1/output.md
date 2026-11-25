## REFORMULACION

**Propósito:** que el modo incremental de sldb funcione entre procesos persistiendo el conjunto de documentos sucios, hoy solo en memoria.

**Resultado:** `documents_dirty.json` en el `.sldb_cache` del store, con `{"signature": ..., "entries": [[modelo, namespace, [nombres...]], ...]}`; escritura atómica (tmp + `os.replace`) bajo `store_lock`; carga perezosa en la primera `names()` del store; `mark`/`clear`/`invalidate` reescriben el archivo; corrupto → borrar archivo y `names()` devuelve `None` sin log ni error. Lógica en módulo nuevo `documents_dirty_persist.py` para que `documents_dirty.py` no pase de 80 líneas.

**Repo:** `SLDB_1`, paquete `sldb.store`; tests en `tests/store/test_merkle_operation_cache.py`; CHANGELOG.

**Límites:** no versionar el archivo, no cambiar qué se considera sucio.

## AMBIGUEDADES

1. "invalidarlo cuando cambia la firma del store" — no dice si al detectar firma distinta se borra el archivo, se descarta en memoria o se recalcula; obliga a inventar el mecanismo.
2. "mark, clear e invalidate reescriben el archivo entero" — no dice si esos métodos hacen carga perezosa antes de reescribir; sin ella machacarían entradas de otros modelos. Obliga a inventar el orden carga-escritura.
3. "la primera llamada a `names()` para un store lee el archivo una vez y llena `_DIRTY`" — no aclara si la comparación de firma ocurre solo en esa carga o en cada `names()`.
4. `clear_all()` existe en `documents_dirty.py` pero la persistencia no lo menciona: ¿borra el archivo, lo vacía, lo ignora? Obliga a decidir.
5. "invalidate(s_path, model_name)" no recibe namespace, pero "reescriben el archivo entero": ¿invalida todos los namespaces del modelo? Inferible pero no explícito.

## DRY-RUN

**Lecturas:** `documents_dirty.py`, `user_cache.py`, `runtime_cache_signature.py`, `io/__init__.py` (`store_lock`), consumidores de `names`/`mark`/`clear`, tests store existentes.

**Cambios previstos:** crear `sldb/store/documents_dirty_persist.py`; adelgazar `documents_dirty.py` para delegar; añadir tests (proceso nuevo ve el dirty del anterior; archivo corrupto cae al cálculo completo) en `test_merkle_operation_cache.py`; entrada en CHANGELOG.

**Dependencias:** `store_lock`, `runtime_cache_signature.signature`, `json`, `os.replace`.

**Validaciones futuras:** los cinco comandos de Validation del TaskDoc (`test_merkle_operation_cache.py`, `test_runtime_wiped.py`, `test_edges_follow_the_contract.py`, `test_clean_code_rules.py`, `tools/check.sh --fast`). No se ejecuta nada aquí.

## FUTURO

Un ejecutor implementará y correrá las validaciones; un humano o `deskops closeout` decidirá el commit, la retirada de pills obsoletas y el cierre de la tarea en el Board.

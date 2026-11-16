# Executor deskops-e-4e4ba795934b — LISTO (antes BLOQUEADO; ver "Tras la decisión (a)")

Tarea: task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444

## Motivo
El contrato y el brief chocan en la superficie exacta del cambio:

- El Implementation Path exige editar:
  1. `src/sldb/api/documents/apply_batch.py` (tomar `store_lock(..., wait=True)` alrededor de prevalidación + `transaction()`, pasar `expected_source_hash`/`expected` a `tx.update`);
  2. `src/sldb/store/io/lock.py` (hacer `StoreIOLock` reentrante por proceso);
  3. `tests/api/test_apply_batch_lock.py` (test de dos procesos; el contrato sugiere ese nombre).
- El brief ("Árbol compartido") declara esos mismos tres archivos como cambios ajenos sin commitear y prohíbe tocarlos, stagearlos o revisarlos.

Estado observado (sin abrir los diffs, solo `git status`/`ls`), HEAD 576cd38f:
- ` M src/sldb/api/documents/apply_batch.py` (+12/-? líneas)
- ` M src/sldb/store/io/lock.py` (+23 líneas)
- `?? tests/api/test_apply_batch_lock.py` (3823 B, mtime 2026-11-15 23:48)

Probablemente son un intento previo de esta misma tarea. No hay forma de cumplir Goal/Done When sin editar esos archivos (el cerrojo y la reentrancia viven en lock.py; el lote, en apply_batch.py), y no improviso un módulo paralelo fuera del Scope.

## Archivos tocados
Ninguno del código. Solo escribí en este directorio: `result-summary.md` y `validation.log`.

## Comandos corridos
- `git status --short -- src tests` rc=0
- `git diff --stat` rc=0
- No corrí Validation: no hay cambio propio que validar.

## Para desbloquear (decisión del coordinador)
a) Declarar que los cambios en esos tres archivos son de esta tarea y autorizarme a revisarlos/completarlos; o
b) que su dueño los commitee/descarte y relanzar con el árbol limpio en esos archivos.


---

## Tras la decisión (a)

El coordinador declaró que los cambios sin commitear de `apply_batch.py`, `lock.py` y
`tests/api/test_apply_batch_lock.py` son de esta tarea (un intento del piloto scion que quedó en pausa).
`uv.lock` sigue siendo ajeno y no lo toqué.

### Revisión contra el contrato y cambios
- `src/sldb/api/documents/apply_batch.py` · `apply_batch`: **queda como estaba** (ya cumplía). Toma
  `store_lock(location.store_path, wait=True)` envolviendo `prevalidate_changes` y `transaction()` hasta
  la última escritura. `_APPLY["update"]` pasa `expected_source_hash`/`expected` a `tx.update`.
  `move`/`untrack`/`delete` no admiten guardas en `Transaction`: los cubre la prevalidación, que ahora
  corre bajo el mismo cerrojo (lo que el contrato admite). Las excepciones no cambian: `ConflictError`
  para un guarda y `SLDBStoreError` "busy" sin wait.
- `src/sldb/store/io/lock.py`: la reentrancia ya existía, pero `_acquire_outer` tenía 13 líneas de lógica
  y violaba `test_clean_code_rules`. Lo reescribí así:
  - `_counted(key)` es un contextmanager de módulo que incrementa y decrementa `_HELD[key]` y borra la
    clave al llegar a 0.
  - `StoreIOLock.acquire` reutiliza el cerrojo si el proceso ya lo tiene y solo cuenta; si no, usa
    `_locked_fd(wait)` + `_counted(key)`.
  - `StoreIOLock._locked_fd` es el cuerpo original de HEAD (abre el fd, bloquea, `LOCK_UN`, cierra).
  - Los llamadores no anidados se comportan igual que en HEAD. Nota: `_HELD` es por proceso y no por
    hilo, igual que `lockf` (POSIX), que ya permitía a otro hilo del mismo proceso entrar.
  - 77 líneas en total.
- `tests/api/test_apply_batch_lock.py`: lo corregí porque el original **no probaba la carrera**. Con el
  cerrojo de lote quitado de `apply_batch` seguía pasando: el 2.º proceso tarda más de 1 s en importar,
  así que nunca competía. Cambios:
  - Hay marcadores: el 2.º proceso escribe `started` justo antes de `apply_batch` y `entered` al
    prevalidar. El test espera `started` y comprueba que `entered` **no** aparece mientras el 1.º retiene
    el cerrojo.
  - Cada lote lleva dos cambios: un update guardado de `login` y un create `extra-<title>`. El perdedor
    recibe `ConflictError` y no escribe nada: `extra-loser.md` y su shard no existen, y `login.md` no
    contiene "Loser".
  - Comprueba los hashes: el `source_hash` del índice es igual al sha256 de los bytes de `login.md` y
    distinto del hash inicial.
  - Comprueba la integridad: `check_store(...)["ok"]` sobre el store de `tmp_path`.
  - Quité los imports y helpers sin uso (`_tree`, `StoreIOLock`, `PAYLOAD`).
- Pruebas de mutación hechas a mano y revertidas (copia en /dev/shm; nada quedó cambiado):
  - Sin `store_lock` en `apply_batch`: el test de concurrencia **falla** (`entered` existe).
  - Con `lock.py` de HEAD (no reentrante): **falla** (el 1.º proceso sale con "busy").

### Done When
- Test con dos procesos reales sobre un store copiado: el guarda rechaza con `ConflictError` y no hay
  escritura parcial. Está cubierto por `test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write`.
- Tests de a un archivo: OK. `tools/check.sh` completo: rc=1, pero las fallas no las causa este cambio
  (ver abajo). `stores build --check`: delegado al integrador.

### Comandos (salida completa en validation.log; todos con TMPDIR=/dev/shm y `uv run --frozen --extra code --extra dev`)
| comando | rc |
|---|---|
| pytest -q tests/api/test_apply_batch_lock.py | 0 (2 passed) |
| pytest -q tests/api/test_transaction.py | 0 (13) |
| pytest -q tests/api/test_transaction_rules_dirty.py | 0 (4) |
| pytest -q tests/api/test_write_paths_validate.py | 0 (5) |
| pytest -q tests/api/test_on_write_entering.py | 0 (7) |
| pytest -q tests/store/test_update_fault_tolerance.py | 0 (5) |
| pytest -q tests/test_clean_code_rules.py | 0 (1168 passed; antes fallaba en lock.py) |
| bash tools/check.sh --fast | 0 |
| flock … bash tools/check.sh | 1 — fallan 'afirmaciones' y 'pruebas', ninguna por este cambio |
| flock … sldb stores build --check | no corrido: detenido por orden del integrador, delegado al integrador |

Las dos fallas de `tools/check.sh` (full):
- **'afirmaciones'** (11 falsas): están en `docs/architecture/{evidence-model-family,references,selectors,views}.md`
  y `CHANGELOG.md` (`docs/missing`, `docs/ambiguous`, `sldb query`, `sldb models describe`). No toqué
  ningún doc ni el CHANGELOG, y mi cambio no toca la CLI: son preexistentes y ajenas a esta tarea.
  `check.sh --fast`, que incluye la puerta de afirmaciones del CHANGELOG del brief, da rc=0.
- **'pruebas'**: 2 failed y 46 errors, **todos en `tests/mcp/`**:
  - 47× `ModuleNotFoundError: No module named 'anyio'`.
  - 2 asserts que reciben "sldb mcp needs the optional `mcp` extra".
  - Causa: el `.venv` se sincronizó con `--extra code --extra dev`, sin el extra `mcp`. Es un problema
    del entorno, no de este cambio.
  - El resto: 2958 passed, 7 skipped, 1 xfailed.

### `stores build --check`
Mi `flock /dev/shm/sldb1-tests.lock … sldb stores build --check` estuvo esperando el cerrojo (lo
retenía la suite de integración) y lo detuve por orden del coordinador sin que llegara a ejecutarse.
Por orden del integrador **ese chequeo queda delegado al integrador**.

### Archivos tocados
- `src/sldb/store/io/lock.py` (modificado sobre el cambio del piloto)
- `tests/api/test_apply_batch_lock.py` (reescrito en parte)
- `src/sldb/api/documents/apply_batch.py`: revisado, sin cambios respecto del cambio del piloto
- `runs/subagents/20261116-exec-guardas/{result-summary.md,validation.log}`
- No hice ningún stage ni commit, y no toqué `desk/`, `.sldb/` ni `uv.lock`.

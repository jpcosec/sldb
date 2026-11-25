Eres el ejecutor de UNA tarea del desk de sldb (repo /mnt/ssd/proyectos/SLDB_1/sldb). Implementas y validas; NO cierras la tarea ni tocas el Board.

## Reglas de trabajo
- Trabaja en /mnt/ssd/proyectos/SLDB_1/sldb en la rama main, SIN worktrees ni ramas nuevas.
- Hay otro worker con archivos sucios en sldb (.sldb/, desk/, uv.lock): toca y commitea SOLO tus propias rutas (src/, tests/ y tu run dir). Nunca toques ni stagees lo ajeno.
- Nunca escribas a mano en desk/ ni en .sldb/ (desk solo con deskops, .sldb solo con sldb). Nunca pgrep/pkill. Pon `timeout` delante de lo que pueda colgarse.
- Evidencia y notas: run dir runs/subagents/20261116-apply-batch-guardas/ (escribe ahí result-summary.md y validation.log con los comandos y salidas reales). Nada de /tmp.
- Tests puntuales, uno a la vez y sin lock: `TMPDIR=/dev/shm pytest -q <archivo>`.
- La suite completa UNA sola vez, al final: `TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock pytest -n 4 -q`.
- Después: `tools/check.sh` y `sldb stores build --check`. Si falla algo ajeno a tu cambio, documéntalo en validation.log y no lo arregles.
- Commit en castellano, con rutas nombradas (nunca `git add -A` ni `git add .`), trailer final exacto `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. SIN push. Incluye en el commit tu run dir.
- Al terminar borra lo tuyo en /dev/shm (tmp de tests, copias de store).
- Termina con `sciontool status task_completed "<sha y resumen>"` (o `sciontool status blocked`/`ask_user`/`limits_exceeded` si procede).

## La tarea (salida de `deskops show task <id> --root /mnt/ssd/proyectos/SLDB_1/sldb` y cuerpo del TaskDoc)
# apply_batch: guardas expected_source_hash bajo el cerrojo del store (inbox 20261115-022444)

## Rationale

_Explain why this task exists or the business driver behind it._

Con dos procesos escribiendo, otro puede cambiar un documento entre la comprobación del guarda y la escritura; el guarda no lo ve.

## Goal

_Describe the concrete result this task must produce._

apply_batch sostiene el cerrojo del store desde la prevalidación hasta la última escritura, y los guardas se comprueban dentro de la transacción.

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-022444. Hoy los guardas se comprueban en la prevalidación y la aplicación no los recibe; el cerrojo StoreIOLock se toma por escritura de índice. Tomar el cerrojo en todo el lote, comprobar guardas dentro, test con dos procesos que prueba que no hay escritura parcial ni guarda saltado. Prerrequisito del lote inverso (inbox 20261115-123855) porque el inverso lleva guardas del estado que dejó el lote.

## Implementation Path

_Outline the expected implementation route or affected surface._

Superficie real (leída en src/): src/sldb/api/documents/apply_batch.py (hoy: prevalidate_changes fuera de todo cerrojo, luego transaction(); _APPLY llama tx.update(id, payload) SIN guardas); src/sldb/api/documents/batch_prevalidate.py (check_guards(location, m_entry, doc, expected_source_hash, expected, pythonpath) lanza ConflictError de sldb.core.exceptions.sldb_conflict_error); src/sldb/api/documents/transaction_ops.py (update ya acepta expected_source_hash y expected y llama check_guards); src/sldb/api/documents/transaction.py (Transaction.update(ref, payload, expected_source_hash=None, expected=None)); cerrojo: sldb.store.io.store_lock(store_path, wait=False) -> StoreIOLock.acquire en src/sldb/store/io/lock.py (fcntl.lockf sobre lock_path(store_path)). 1) apply_batch toma store_lock(location.store_path, wait=True) envolviendo prevalidación Y transaction() hasta la última escritura; wait=True para que el segundo proceso espere y vea el estado nuevo (con wait=False saldría SLDBStoreError busy, no ConflictError). 2) Los guardas se comprueban dentro del cerrojo: se conserva la prevalidación (ahora bajo cerrojo) y además se pasan expected_source_hash/expected a tx.update (y a los demás actions sobre documentos rastreados si transaction_ops los admite; si no, la prevalidación bajo el mismo cerrojo ya es atómica). Sin reentrancia hoy: fcntl.lockf es por proceso y os.close del fd interior libera el cerrojo exterior (semántica POSIX), y otros caminos dentro de la transacción (index_commit, untrack_document, rebuild_edges, etc.) llaman store_lock; el ejecutor debe hacer StoreIOLock reentrante dentro del proceso (contador por store_path resuelto, solo el exterior abre fd, bloquea y cierra) o demostrar con test que no se pierde el cerrojo, sin cambiar el comportamiento de los demás llamadores. 3) Excepciones sin cambio: ConflictError para guarda, SLDBStoreError si ocupado sin wait. 4) Test nuevo en tests/api/ (p.ej. tests/api/test_apply_batch_lock.py) con dos procesos reales (subprocess o multiprocessing 'spawn') sobre un store copiado a tmp_path (ver fixture api_store en tests/api/conftest.py y tests/api/test_transaction.py como patrón): ambos lotes llevan expected_source_hash del mismo estado inicial; uno gana, el otro recibe ConflictError y no deja escritura parcial (comprobar hashes y que stores build --check sigue limpio); sincronizar con Event/archivo para que el segundo llegue mientras el primero retiene el cerrojo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Test de concurrencia con dos procesos reales sobre un store copiado: el guarda rechaza como ConflictError sin escritura parcial; suite de a un archivo, tools/check.sh y stores build --check.

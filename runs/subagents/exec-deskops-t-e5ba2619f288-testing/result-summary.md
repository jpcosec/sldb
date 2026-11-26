PASA

# Tester deskops-t-e5ba2619f288: undo_changes entre sesiones desde el registro de lotes del store

Task: `task-undo-changes-deshace-un-cambio-aplicado-en-una-sesion-anterior-porque-el-registro-de-movimientos-per`
Commit revisado: `e1c234372b8aaa4e48c591aeb3e8c36090d11802` — `feat: undo_changes deshace lotes entre sesiones desde el registro de lotes del store`.
El commit no lleva `Task-Id` (como pedía el encargo), así que el `git log --grep "Task-Id: ..."` de «Como probar» no lo encuentra; se localizó por el asunto del commit, justo antes del commit de run `7755e214`.
Archivos: `contracts/layers.toml`, `docs/architecture/journal-authority.md`, `src/sldb/api/__init__.py`, `src/sldb/api/documents/{apply_batch,batch_inverse,batch_report,nothing_to_undo,provenance_stamp,undo_batches,undo_report}.py`, `src/sldb/mcp/{server.py,write/apply.py,write/undo.py}`, `src/sldb/store/write_journal.py`, `tests/mcp/test_write_tools.py`, `tests/test_mcp_undo_across_sessions.py` (+390/−82).

## Veredicto

**PASA.** Cada lote aplicado por `apply_batch`/`apply_batches` queda en el write journal del store (`.sldb/core/write_journal/*.json`) con id de lote, orden, actor, hora, el lote inverso y, por documento, su before-image (modelo, ruta, payload y procedencia; nulo si lo creó) y el hash de contenido que dejó (`after_hash`; nulo si lo borró). `sldb.api.undo_batches` revierte los últimos lotes no revertidos en una transacción bajo el lock; `undo_changes` del MCP lo usa y por tanto funciona desde un proceso distinto del que aplicó. El journal no cuenta en el hash del store: tras deshacer, el hash vuelve al valor anterior aunque el archivo del journal siga existiendo marcado como revertido.

## Validación ejecutada

Entorno: `/tmp/ws-venv` no existe en este contenedor; usé el venv del repo `/workspace/sldb/.venv` (Python 3.13.18) primero en `PATH`, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-e5ba2619f288`. Ese venv no traía el extra `mcp`, por lo que `tests/test_mcp_undo_across_sessions.py` se habría saltado por `importorskip`; instalé `mcp>=2.2,<3` en el mismo venv para ejecutar el test de verdad.

| Comando | rc | Resultado |
|---|---:|---|
| `python -m pytest -q tests/test_mcp_undo_across_sessions.py` | 0 | **3 passed** |
| `python -m pytest -q tests/mcp/test_write_tools.py` | 0 | **13 passed** |
| `python -m pytest -q tests/api/test_apply_batch_dry_run.py` | 0 | **4 passed** |
| `python -m pytest -q tests/api/test_apply_batch_lock.py` | 0 | **4 passed** |
| `python -m pytest -q tests/api/test_journal.py` | 0 | **4 passed** |
| `python -m pytest -q tests/api/test_provenance.py` | 0 | **10 passed** |
| `python -m pytest -q tests/api/test_transaction.py` | 0 | **16 passed** |
| `python -m pytest -q tests/api/test_provenance_index.py` | 0 | **3 passed** |
| `python -m pytest -q tests/api/test_on_write_entering.py` | 0 | **8 passed** |
| `python -m pytest -q tests/api/test_write_paths_validate.py` | 0 | **5 passed** |
| `python -m pytest -q tests -k "mcp and undo"` | 0 | **11 passed, 3355 deselected** |
| `python -m pytest -q tests/mcp/test_mutability.py` | 0 | **7 passed** |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No se corrió la suite completa. No existe `tests/test_write_journal.py`, `tests/test_undo_batches.py` ni `tests/test_batch_inverse.py`; los tests existentes de los módulos tocados son los de `tests/api/` listados arriba, más `tests/mcp/test_write_tools.py`, todos corridos. El test nuevo cubre el requisito de segundo proceso levantando servidores MCP reales por stdio (`served`) que terminan entre lote y lote.

## Cobertura del Done When

- **Un servidor aplica y otro deshace:** `test_a_new_process_undoes_what_another_applied_in_reverse_order` aplica cada lote con un `served(...)` propio (el proceso termina al salir del `with`), lee con otro proceso y deshace con otro. Restaura el título y el `store_fingerprint(...).store_hash` al valor anterior al lote.
- **Dos deshaceres en orden inverso:** el mismo test aplica «first» y «second», deshace una vez y comprueba título `first` y hash `h1`, deshace otra vez y comprueba el original y `h0`; el tercer intento responde `nothing_to_undo` sin escribir.
- **Id solo para el último no revertido:** `test_an_id_is_accepted_only_for_the_last_not_reverted_batch` rechaza el id del lote viejo con `nothing_to_undo`, sin tocar el árbol (`tree_digest`), y luego acepta el nuevo y después el viejo.
- **Documento cambiado después:** `test_a_batch_whose_document_changed_afterwards_is_refused_and_nothing_is_written` edita el documento fuera de lote con `save_document_payload`; `undo_changes` responde `stale`, `written: False`, nombra el documento y deja el árbol byte a byte igual.
- **Hash del store sin el journal:** el retorno a `h0`/`h1` ocurre con los archivos del journal todavía presentes (marcados `reverted_at`), así que el test demuestra que el journal no participa del hash.
- **Guardas de la sesión anterior:** `tests/mcp/test_write_tools.py` conserva los casos de conflicto, cadena whole-or-nothing, vuelta al mismo contenido (no stale), y «nada que deshacer»; adapta los tests a una copia propia porque el journal ahora es del store y no de la sesión.

## Revisión del cambio

- `write_journal.record` escribe un JSON por lote de forma atómica (`.tmp` + `replace`) bajo el lock del store; `entries` los ordena por `order` y `unreverted` filtra `reverted_at`.
- `apply_batch` registra el lote después del commit pero dentro del lock; `apply_batches` registra cada lote de la transacción. Un `dry_run` no registra nada.
- `undo_batches` elige los últimos `steps` no revertidos (de más nuevo a más viejo), los aplica como una cadena en una sola transacción y solo después los marca revertidos. `batch_id` solo se acepta si coincide con el último no revertido; si no, `NothingToUndo` con el id del último.
- El deshacer fija la procedencia previa de cada documento (`pinned_provenance`), por eso el hash del store vuelve al valor anterior; la guarda de conflicto sigue comparando contenido sin procedencia, como antes.
- `undo_changes` ya no mantiene pila en memoria: lee el journal del store y responde `remaining` desde él. El cambio de instrucciones del servidor describe el nuevo alcance entre sesiones.
- `docs/architecture/journal-authority.md` documenta el registro de lotes como extensión del mismo sustrato (no un registro paralelo), y `contracts/layers.toml` mapea `store/write_journal.py` al eje `bitacora`.

## Observaciones no bloqueantes

- `tests/mcp/test_no_writes.py::test_every_read_tool_leaves_the_store_untouched` falla, pero es ajeno a este commit: `tests/mcp/test_read_tools.py` ya incluía `anchors_resolve` en `TOOLS` desde `f68074750` y `test_no_writes.py` no lo llama. Verifiqué que ambos hechos ya están en el padre `e1c2343^`; ni el test ni esa superficie cambian en el commit revisado. No entra en las validaciones pedidas.
- `apply_batch` aplica la transacción y luego escribe el journal; un fallo de disco justo entre ambos dejaría el lote aplicado sin entrada de deshacer. No hay requisito de atomicidad journal↔commit en el encargo y el caso no está cubierto por ningún test.
- El journal es del store, no del actor: `undo_changes` sin id revierte el último lote no revertido aunque lo haya aplicado otra persona. Es coherente con «el registro es del sustrato» y con el Done When; conviene tenerlo presente si más adelante se quiere deshacer por actor.

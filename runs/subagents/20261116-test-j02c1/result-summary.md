# Tester deskops-t-d1b6e7f699fb: corrección de j02 (AGENTS.md en identidad, derived_guard sin núcleo)

**Veredicto: PASA.** Salida completa en `validation.log`.

## Cambio revisado (sin commitear)
- `tools/check_identity.py`: `"AGENTS.md"` en `EXEMPT`, con comentario de guía de procedimientos para agentes (merge de .sldb).
- `src/sldb/store/io/derived_guard.py`: `from sldb.core.exceptions import SLDBStoreError` → `from sldb.store.exceptions import SLDBStoreError` (el seam que ya usan `io/rollback.py` e `io/lock.py`). Está fuera de `files`, pero el punto 2 del Scope lo autoriza explícitamente.
- `tests/store/test_update_fault_tolerance.py`: sin cambios.

## Validation (corrida por mí, `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`)
| comando | resultado |
|---|---|
| pytest -q tests/test_store_seams.py | PASA, 2 passed (en HEAD: 1 failed, `io/derived_guard.py: sldb.core.exceptions`) |
| pytest -q tests/store/test_update_fault_tolerance.py | PASA, 8 passed |
| pytest -q tests/store/test_merkle_shards.py | PASA, 6 passed |
| pytest -q tests/test_clean_code_rules.py | PASA, 1193 passed |
| bash tools/check.sh --fast | PASA, rc=0, «TODAS LAS PUERTAS PASAN»; identidad: 0 violaciones (omitidas por --fast: afirmaciones, pruebas, selfdoc, como corresponde a --fast) |

No se corrió la suite completa ni `sldb stores build --check` (el contrato no los nombra; quedan delegados al integrador).

## Done When, punto por punto
- **Validation pasa, incluidos seams y check.sh --fast con todas sus puertas**: PASA (tabla de arriba).
- **El error de un índice derivado con marcadores sigue nombrando el comando exacto**: PASA. El texto de `unmerged_index_error` no cambió; el test `test_a_conflicted_derived_index_says_which_command_to_run` compara el mensaje exacto y pasa; mi script lo confirma vía API y vía CLI (`sldb stores check` y `sldb docs list` salen con `SystemExit` con el mensaje exacto).
- **Misma clase de excepción para quien la atrapa**: PASA. `sldb.store.exceptions.SLDBStoreError is sldb.core.exceptions.SLDBStoreError` (reexport, mismo objeto). Quién la atrapa: `sldb/cli/main.py:31` (`isinstance(e, SLDBError)` → `SystemExit(str(e))`, importado de `sldb.core.exceptions`), `guarded_load` mismo (`except (FileNotFoundError, SLDBStoreError): raise`), los lectores `load_store_index`/`load_models_index` en `sldb/store/io/__init__.py:82,88`, y el test que hace `pytest.raises(sldb.core.exceptions.SLDBStoreError)`. MRO: SLDBStoreError → SLDBError → StoreError; `isinstance` con las tres pasa.
- **commit**: no lo hace el tester (prohibido en el brief); queda para el integrador.

## Casos que el ejecutor no cubrió (scripts en /dev/shm/j02c1t, sin tocar el repo)
1. Marcadores diff3 (`|||||||` base) en `store_index.yaml` de un store creado con `sldb stores init`: error exacto vía API y vía CLI (`stores check`, `docs list`). PASA.
2. Caso negativo de la puerta de identidad en una copia `git archive HEAD`: en HEAD falla por AGENTS.md (reproduce el fallo del integrador); con el fix pasa; con el fix y un `ROGUE.md` versionado en la raíz, la puerta sigue fallando (`archivo versionado sin clasificar en la raíz: ROGUE.md`, rc=1). La exención es puntual y no abre la puerta. PASA.

## Alcance
`git diff --name-only`: aparte de los dos archivos de la corrección solo están `.sldb/core/models/{InboxNoteDoc,RunDoc}.yaml`, `.sldb/core/store_index.yaml` y `.sldb/store.yaml`; son los registros del despacho (RunDoc de exec/test j02c1 y 2 notas de inbox), no del ejecutor. Los cambios ajenos que lista el brief (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`) ya no aparecen como modificados en el árbol; no los toqué. PASA.

## Regresiones vecinas
Módulo de `src/` cambiado: `sldb.store.io.derived_guard`. Ningún test lo importa por nombre; corrí los 44 archivos de `tests/` que importan el paquete `sldb.store.io`, uno por uno: **44/44 pasan, 0 fallas**. El cambio solo cambia la ruta de import de la misma clase, así que no hay comportamiento distinto en tiempo de ejecución.

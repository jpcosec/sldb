# Tester deskops-t-eab6088c807b — veredicto: **PASA**

Tarea: `task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l`
Base de comparación: HEAD `12e9b191`, extraído con `git archive` en `/dev/shm/t-ci2-head`.
Scripts propios: `/dev/shm/t-ci2-scripts/{edge,conc,race}.py`. No se editó el repo.
Salida completa: `validation.log`.

## 1. Validation (corrida por mí, todo con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)

| Comando | Resultado | rc | Veredicto |
|---|---|---|---|
| `pytest -q tests/api/test_api_documents.py` | 17 passed (incluye los 4 tests nuevos) | 0 | PASA |
| `pytest -q tests/api/test_on_write_entering.py` | 7 passed | 0 | PASA |
| `pytest -q tests/api/test_api_stores.py` | 12 passed | 0 | PASA |
| `pytest -q tests/test_links_batch_cli.py` | 5 passed | 0 | PASA |
| `pytest -q tests/test_clean_code_rules.py` (obligatorio) | 1177 passed | 0 | PASA |
| `bash tools/check.sh --fast` (obligatorio) | sin salida de error | 0 | PASA |

`uv` funcionó y no hizo falta el fallback. Validation no nombra la suite completa ni `stores build --check`, así que no hubo nada que delegar al integrador.

## 2. Done When, punto por punto

| Punto | Veredicto | Evidencia |
|---|---|---|
| Validation pasa con los tests nuevos | PASA | §1 |
| `make world` de pron con rc 0 contra este sldb | PASA (en logs, aclaración 2) | Según la aclaración 2 revisé los logs y no repetí la corrida. El control C, `pron-world-layout-head.log` (venv `ci2-venv-head`, HEAD sin parche), termina en `ops.py ... _pre_check ... SLDBStoreError: Doc 'rt-implements' already tracked.`, `Makefile:31` y `rc=2`, que es el error del CI. El B, `pron-world-layout-fixed.log` con el parche, pasa `init --world` y `docs` y termina en `rc=0`: solo hay avisos de "Skipped missing documents: reltype-*", sin error. El A, `pron-world-ci2-pron.log` (`/dev/shm/ci2-pron`), da `rc=2` en `Makefile:32` por `No store_index.yaml at /herramientas/deskops/.sldb`: es el enlace de layout de pron hacia deskops, no track. |
| CHANGELOG | PASA | Hay una entrada en 0.1.13 y coincide con el diff. La puerta de afirmaciones de `check.sh --fast` pasa. |
| Commit | No aplica al tester | Sin commitear, como corresponde: lo hace el coordinador. |
| Aviso a sldb-ui y pron | No aplica al tester | Lo hace el coordinador. |

## 3. Scope, comprobado con evidencia propia (`edge.py`)

- **(1) Misma ruta con force: re-indexa.** PASA. Ruta absoluta y `./sub/../login.md` re-indexan: el payload sale del archivo nuevo, `hash_c` del shard es igual al sha256 del archivo y `check_store` da ok. `sldb docs track --model TicketDoc <path> --name login --force` por CLI da rc 0.
- **(2) Otra ruta con force: falla nombrando las dos.** PASA. `moved/login.md` da `SLDBStoreError: Doc 'login' already tracked at 'login.md', not 'moved/login.md'; use move.` y el documento original no cambia.
- **(3) Sin force no cambia (aclaración 4).** PASA. Parcheado y HEAD dan exactamente lo mismo:
  - API: `sldb.core.exceptions.sldb_store_error.SLDBStoreError: Doc 'login' already tracked.` (mismo módulo, misma clase y mismo texto).
  - CLI: rc 1 y última línea de stderr `Doc 'login' already tracked.` en los dos.
- **(4) Docstring y ayuda.** PASA. Están en `track_document_file.py` y en `docs1.py`. `docs1.py` está autorizado por la aclaración 1.
- **(5) Tests.** PASA. Son los cuatro del contrato. El de idempotencia compara bytes de los shards e índices y de `store.yaml`.
- Un documento nuevo con force se trackea como antes.

## 4. Casos que el ejecutor no cubrió

- La ruta escrita de otra forma (absoluta, o `./sub/../login.md`) cuenta como la misma ruta: PASA.
- Re-track con force por CLI: PASA.
- **Concurrencia con force (aclaración 3), `conc.py`:** 6 rondas. En cada una se edita el archivo y luego 3 procesos re-trackean `login` con force 5 veces a la vez. Al final de cada ronda, `check_store` en un proceso nuevo da `ok: true`, sin `mismatched`, `damaged` ni `alerts`, y `hash_c` del shard es igual al sha256 del archivo. **PASA.** En una de las 18 corridas un hijo terminó con `SLDBStoreError: Store at ... is busy. Use --wait to block.`. Es el rechazo sin espera de `store_lock`, que el parche no toca (`lock.py` no es parte del diff), y el índice quedó coherente igual.
- **Carrera sin force sobre un documento nuevo, `race.py`:** 4 procesos, 5 veces. En cada vez exactamente uno da OK y los otros 3 `SLDBStoreError Doc 'raceN' already tracked.`; `check_store` da ok. Confirma que el segundo `_pre_check` bajo `store_lock` reemplaza bien al que se quitó de `_do_track`. **PASA.**
- Observación, no es falla: un re-track con force de un documento trackeado cuyo archivo ya no existe da `FileNotFoundError` crudo. Antes daba `already tracked`. Está fuera del Scope y es el mismo error de un track normal sobre un archivo inexistente.
- Observación, no es falla y es anterior al parche: en un proceso que ya leyó el store, `load_runtime_documents` no ve una re-indexación hecha por otro proceso hasta la siguiente operación. Es la caché por operación de `runtime_cache_signature`.

## 5. Nada tocado fuera del contrato

`git diff --name-only` en `src/`, `tests/` y `CHANGELOG.md` da `src/sldb/store/ops.py`, `src/sldb/api/documents/track_document_file.py`, `src/sldb/cli/parsers/docs1.py` (aclaración 1), `tests/api/test_api_documents.py` y `CHANGELOG.md`. También están modificados `.sldb/core/models/{InboxNoteDoc,RunDoc}.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y RunDoc/InboxNote nuevos. Son el registro del desk (RunDoc de executor y tester, nota del inbox 193112), no del ejecutor. Los cambios ajenos que lista el brief no se revisaron. `apply_batch.py`, `lock.py`, `test_apply_batch_lock.py` y `uv.lock` ya no aparecen modificados en el árbol.

## 6. Regresiones vecinas

Módulos de `src/` cambiados: `store/ops.py`, `api/documents/track_document_file.py` y `cli/parsers/docs1.py`. Busqué con `grep -rl` en `tests/` los archivos que usan `track_document_file`, `track_document`, `StoreOperations`, `sldb.store.ops`, `docs1` o `docs track`: son 40, sin contar `conftest.py`. Corrí cada uno por separado: **40/40 pasan, 0 fallas** (lista en `validation.log`). Como nada falla, no hizo falta comparar contra HEAD.

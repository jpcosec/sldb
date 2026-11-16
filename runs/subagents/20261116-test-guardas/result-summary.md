# Tester deskops-t-a6ddcc3e4afc — PASA

Tarea: task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444
HEAD 576cd38f (+ e138ff19). Alcance revisado según la aclaración del coordinador: el cambio de esta tarea es
`src/sldb/api/documents/apply_batch.py`, `src/sldb/store/io/lock.py` y `tests/api/test_apply_batch_lock.py`.
`uv.lock` es ajeno y no lo revisé. Salida completa en `validation.log`. Todo con
`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev` (uv funcionó, no hizo falta usar uvx).

## Validation
| punto | veredicto | evidencia |
|---|---|---|
| pytest de los archivos tocados, de a uno | PASA | `tests/api/test_apply_batch_lock.py`: 2 passed, rc=0 |
| `tools/check.sh` | PASA (`--fast`) / el completo no se corrió | `--fast`: "TODAS LAS PUERTAS PASAN", rc=0. No corrí el completo porque incluye la suite completa ("pruebas"), que el brief prohíbe. Corrí aparte su puerta 'afirmaciones' (ver abajo) |
| `sldb stores build --check` | delegado al integrador | prohibido por el brief, no se corrió |
| `tests/test_clean_code_rules.py` (siempre) | PASA | 1168 passed, rc=0. `lock.py` cumple las reglas: 77 líneas, funciones ≤10 de lógica, 1 clase |

## Done When
- **Test de concurrencia con dos procesos reales sobre un store copiado: el guarda rechaza con ConflictError y no hay escritura parcial.** PASA.
  - `test_second_process_with_the_same_guard_conflicts_and_leaves_no_partial_write` usa `subprocess` sobre el store de `tmp_path`. Comprueba:
    - que el 2.º proceso no entra a prevalidar mientras el 1.º retiene el cerrojo;
    - que el resultado es OK/CONFLICT;
    - que no se escribió ni el update ni el create del perdedor;
    - que el `source_hash` del índice coincide con el sha256 del archivo;
    - que `check_store` da ok.
  - Mutaciones mías (copias en /dev/shm, el repo no se tocó):
    - Con el `apply_batch.py` de HEAD, el test **falla** (`assert not (tmp_path/"entered").exists()`).
    - Con el `lock.py` de HEAD (sin reentrancia), **fallan** los dos tests: el 1.º proceso muere y queda `('', 'OK')`, y la reentrancia da `'GOT' == 'BUSY'`.
  - Conclusión: el test discrimina de verdad.
- **Suite de a un archivo.** PASA. Ver regresiones vecinas.
- **`tools/check.sh`.** PASA en `--fast`. Las fallas del check completo ya estaban en HEAD:
  - **'afirmaciones'** (`tools/check_claims.py`): árbol actual y HEAD (`git archive` en /dev/shm/tg-base) dan la **misma** salida, 11 falsas en docs/architecture/* y CHANGELOG.md, rc=1 en ambos. No las causa este cambio, que no toca docs, CHANGELOG ni la CLI.
  - **'pruebas' en tests/mcp**: `tests/mcp/test_dry_run.py` falla igual en el árbol actual y en HEAD (`ModuleNotFoundError: No module named 'anyio'`). En el venv `anyio` y `mcp` no están instalados porque falta el extra `mcp`. Es un problema del entorno. `tests/mcp/test_cli_mcp.py` pasa en ambos (3 passed).
- **`stores build --check`.** Delegado al integrador.

## Casos no cubiertos por el ejecutor (script en /dev/shm/tg-edge/test_tester_edges.py): 6 passed
- **Guarda obsoleto en `delete`, `move` y `untrack` desde un 2.º proceso** mientras el 1.º lote retiene el cerrojo: da ConflictError. `login.md` y su shard siguen existiendo y `moved.md` no existe.
  - Esto confirma que la prevalidación bajo el cerrojo protege las acciones que `Transaction` no guarda.
- **Otro proceso con `store_lock` sin wait mientras el lote retiene el cerrojo**: da `SLDBStoreError` busy. Las excepciones no cambiaron.
- **ConflictError dentro del proceso**: el cerrojo se libera (`_HELD` queda vacío y otro proceso lo obtiene).
- **Excepción en un `store_lock` anidado**: el exterior sigue retenido (el otro proceso ve BUSY) y al salir se libera.
- **Ruta relativa `.sldb` y ruta absoluta**: comparten el mismo contador, porque la clave es `resolve()`.

## Regresiones vecinas (módulos cambiados: `sldb.api.documents.apply_batch` y `sldb.store.io.lock`/`store_lock`)
- Archivos de tests que importan alguno de esos módulos (con `grep -rl`):
  - `test_apply_batch_lock`, `test_transaction`, `test_write_paths_validate`, `test_on_write_entering`;
  - `tests/store/test_update_fault_tolerance`.
- Corrí además, de a uno, otros que escriben bajo el cerrojo:
  - `test_api_documents`, `test_api_creation`, `test_api_stores`;
  - `tests/store/test_cli_store`, `tests/store/test_stores_build`.
- Resultado: todos rc=0 (2/13/5/7/5/13/6/12/38/27 passed). No hay ninguna falla nueva respecto de HEAD.

## Nada fuera del contrato
- `git status -- src tests tools docs CHANGELOG.md pyproject.toml` muestra solo los tres archivos de la tarea.
- Los cambios en `.sldb/` y `desk/`, en cambio, son de orquestación de otras tareas o de registro de los RunDoc: inbox, reviews, b2/b3 y los `run.md`. No son código del ejecutor.

## Observaciones (no bloquean)
- `_HELD` es por proceso y no por hilo. `sldb serve` usa `ThreadingHTTPServer`: un 2.º hilo que entra mientras el 1.º retiene el cerrojo solo suma al contador y no queda excluido.
  - Si el hilo exterior sale antes, cierra el fd y el cerrojo entre procesos se suelta mientras el otro hilo sigue dentro.
  - En HEAD ya había el mismo hueco, y peor: `lockf` es por proceso y el `close` de cualquier fd soltaba el cerrojo. No es una regresión, pero el contrato del cerrojo sigue sin cubrir hilos.
- Tras un `fork` con el cerrojo retenido, el hijo hereda `_HELD > 0` pero no el `lockf`. Hoy no hay ningún `fork` ni `multiprocessing` en `src/sldb`.

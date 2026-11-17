# Resultado: executor deskops-e-0a2c935f6993 (corrección de j02)

## Cambios
- `src/sldb/store/io/derived_guard.py` (import de módulo): `from sldb.core.exceptions import SLDBStoreError` → `from sldb.store.exceptions import SLDBStoreError`. Es el mismo seam que ya usan `io/rollback.py` e `io/lock.py`; `sldb.store.exceptions` reexporta la misma clase de `sldb.core.exceptions`, así que el tipo y el mensaje del error no cambian (comprobado: `type(unmerged_index_error(p)) is sldb.core.exceptions.SLDBStoreError` → True; el mensaje sigue nombrando `sldb stores rebuild-index` y `sldb stores merge-driver --install`).
- `tools/check_identity.py` (`EXEMPT`): se agrega `"AGENTS.md"` con el comentario fijado por el coordinador: `# AGENTS.md: guía de procedimientos para agentes (merge de .sldb); no es parte del sistema.`
- `tests/store/test_update_fault_tolerance.py`: sin cambios (figura en files; ya pasa).

## Done When
- test_store_seams.py pasa (antes fallaba con `io/derived_guard.py: sldb.core.exceptions`): rc=0.
- check.sh --fast pasa con todas las puertas, incluida la de identidad (AGENTS.md ya está clasificado): rc=0.
- El error de un índice derivado con marcadores sigue nombrando el comando exacto: el texto de `unmerged_index_error` no se tocó.
- Commit: NO hecho, por el brief (prohibido `git commit`) y la decisión 3 del coordinador. Queda para el integrador.

## Comandos (salida completa en validation.log)
| comando (`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`) | rc |
|---|---|
| pytest -q tests/test_store_seams.py | 0 |
| pytest -q tests/store/test_update_fault_tolerance.py | 0 |
| pytest -q tests/store/test_merkle_shards.py | 0 |
| pytest -q tests/test_clean_code_rules.py | 0 (corrido de nuevo después de ajustar el comentario: 0) |
| bash tools/check.sh --fast | 0 (corrido de nuevo después de ajustar el comentario: 0) |

No corrí la suite completa ni `sldb stores build --check`.

## Archivos tocados
- src/sldb/store/io/derived_guard.py
- tools/check_identity.py
- runs/subagents/20261116-exec-j02c1/validation.log, result-summary.md (entrega)

## Desvíos / notas
- `derived_guard.py` no está en `files` del contrato, pero el Scope (punto 2) autoriza corregir el guard de forma explícita, y la decisión 1 del coordinador lo confirma.
- El comentario de EXEMPT usa el texto de la decisión 2 del coordinador, no la redacción libre del Scope.
- No hay pills atados.

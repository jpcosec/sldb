PASA

# Tester deskops-t-336d69094d54: resultado

Task: `task-apply-batch-dry-run-público-que-valida-sin-escribir-inbox-20261115-022430`
Commit revisado: `29c0a85725c47cb27ec460d13be6e54210b3f38e` — `apply_batch: dry_run público que valida sin escribir`
Archivos del commit: `src/sldb/api/documents/apply_batch.py`, `src/sldb/api/documents/batch_report.py`, `tests/api/test_apply_batch_dry_run.py`, `CHANGELOG.md`.

## Veredicto

**PASA.** `apply_batch(..., dry_run=True)` corre `prevalidate_changes` bajo el cerrojo (forma, modelo, round-trip, guardas y destinos), devuelve `BatchReport(applied=False, saved=[], inverse=[], planned=[...])` y vuelve antes de abrir la transacción. Un lote inválido levanta el mismo error que la aplicación real y no deja cambios. `dry_run=False` conserva el camino anterior y `apply_batches` no cambia.

## Validación ejecutada (detalle en validation.log)

Se corrieron de a un archivo, con `TMPDIR=/tmp`:

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q -p no:cacheprovider tests/api/test_apply_batch_dry_run.py` | 0 | 4 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_apply_batch_lock.py` | 0 | 4 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_on_write_entering.py` | 0 | 7 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_transaction.py` | 0 | 15 passed |
| `python -m pytest -q -p no:cacheprovider tests/api/test_write_paths_validate.py` | 0 | 5 passed |
| `python -m pytest -q -p no:cacheprovider tests/mcp/test_write_tools.py` | 0 | 14 passed, 1 xfailed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_apply_batch.py` ni `tests/test_batch_report.py`; los tests del módulo tocado son `tests/api/test_apply_batch_dry_run.py` y `tests/api/test_apply_batch_lock.py`, ambos corridos. No se corrió la suite completa.

Nota de entorno: `/tmp/ws-venv` no existía en el host. Usé el intérprete 3.13.18 de uv con el `site-packages` del `.venv` de sldb (`/workspace/sldb/.venv/lib/python3.13/site-packages`), que es el mismo conjunto de dependencias. El `python` del `.venv` del repo tiene un symlink roto a `/home/robocop/...`, ajeno al commit.

## Comprobaciones adicionales

- **Guards en dry_run:** probé `expected_source_hash`, `expected` y `expected_content_hash` incorrectos; los tres levantan `ConflictError` con el mismo mensaje que la aplicación real y dejan el proyecto byte a byte igual.
- **Sin escritura:** el test nuevo compara hashes SHA-256 de todos los archivos del proyecto y del store antes/después, para lote válido e inválido.
- **Veredicto igual al real:** el test nuevo verifica `planned` y que el lote válido después se aplica de verdad con `saved` en el mismo orden.
- **p3:** `propose_changes` (`src/sldb/mcp/write/tools.py`) no reimplementa la prevalidación ni llama a `prevalidate_changes`; no se tocó, y `docs/architecture/mcp.md` no necesitó cambios.
- **CHANGELOG:** entrada presente y describe `applied`, `planned`, que no evalúa `on_write` y que `apply_batches` no cambia.
- **Alcance:** no hay cambios fuera de los cuatro archivos del commit; las modificaciones de `.sldb/` y `desk/` son del despacho.

## Observaciones no bloqueantes

- `dry_run` no evalúa reglas `on_write`; está documentado en el docstring y en el CHANGELOG, y es coherente con limitar el dry run a la prevalidación.
- La lista `PENDING` de `sldb.mcp.write.pending` todavía menciona el dry run público como pendiente; es una nota del consumidor MCP, no forma parte del alcance de esta task y no afecta el veredicto.

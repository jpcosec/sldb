PASA

# Tester deskops-t-b83af2b6f9cd: resultado

Task: `task-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-actualiza-en-el-mismo-repo-el-store-y-las-refer`
Commit revisado: `bc05f2ab4d1fccca0f3dc22d0a2f7b201ad382c0` — `sldb move: git mv de un archivo o directorio y reescritura de campos y links`
HEAD al probar: `3f547569` (el código de `src/` y `tests/` del commit es idéntico al de HEAD; los commits posteriores solo tocan el store/caché).

## Veredicto

**PASA.** Los tests nuevos y los tests de los módulos tocados pasan, `selfdoc check` queda en 0 y `bash tools/check.sh --fast` termina en 0 con todas las puertas en PASS. No se corrió la suite completa (le corresponde al integrador).

## Validación ejecutada

Se corrieron de a un archivo, con `TMPDIR=/tmp` y el Python 3.13.18 del `.venv` del repo. Detalle completo en `validation.log`.

| Comando | rc | Resultado |
|---|---|---|
| `pytest -q -p no:cacheprovider tests/api/test_move_path.py` | 0 | 9 passed |
| `pytest -q -p no:cacheprovider tests/cli/test_move_cli.py` | 0 | 3 passed |
| `pytest -q -p no:cacheprovider tests/api/test_api_documents.py` | 0 | 21 passed |
| `pytest -q -p no:cacheprovider tests/api/test_transaction.py` | 0 | 16 passed |
| `pytest -q -p no:cacheprovider tests/test_cli_every_command_has_a_handler.py tests/test_cli_format_coverage.py tests/test_cli_envelope.py tests/test_cli_reconciliation.py` | 0 | 18 passed |
| `PYTHONPATH=src python -m sldb selfdoc check` | 0 | `ok: true`, 166 documentos, sin faltantes/cambios/renombres |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

Los dos archivos de test del commit existen y se corrieron. No hay `tests/test_move_path.py`, `tests/test_move_document.py`, `tests/test_move.py` ni `tests/test_relocate_file.py`; los tests que cubren `move_document` y `Transaction` son `tests/api/test_api_documents.py` y `tests/api/test_transaction.py`, también corridos. Para el parser/dispatcher/CLI se corrieron las puertas generales de CLI.

## Comprobaciones de alcance

- El commit agrega `src/sldb/api/documents/move_path*.py`, `relocate_file.py`, `src/sldb/cli/commands/move.py`, el parser y el handler, y `move_document.py` pasa a usar `relocate_file` (`git mv`), como pide el Goal.
- Tests nuevos cubren: renombre git de un documento trackeado y su re-trackeo, campo con la ruta vieja (string y lista), directorio con prefijos (`pkg` vs `pkgzero`), links Markdown relativos (incluye `#ancla`, `./`, bloques fenced y URL externa), `--dry-run` sin cambios y con el mismo informe que la corrida real, destino existente/fuera/inside-itself, y fallo a mitad con restauración del árbol, índice y store.
- `--format json` imprime el informe con `moves`, `fields` y `links`.
- La referencia CLI fue regenerada y `selfdoc check` no reporta cambios; CHANGELOG y `docs/architecture/transactions.md` documentan el comando y sus límites.

## Nota de entorno

`/tmp/ws-venv` no existía en este host. Usé `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python` (3.13.18), el venv del propio repo; para `tools/check.sh` puse ese `bin` primero en `PATH`.

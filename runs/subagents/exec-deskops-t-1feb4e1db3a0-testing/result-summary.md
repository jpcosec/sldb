PASA

# Tester deskops-t-1feb4e1db3a0: docs track --reindex

Task: `task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for`

Commit del ejecutor: `5d0ef9be125f1795815aaed7f997ec9df96b55e4` (`Task-Id` en el mensaje).

## Veredicto

PASA. El commit implementa `--reindex` en el parser y en `DocCLI.track`, y `reindex=True` en
`track_document_file`. Para un documento ya trackeado en la misma ruta re-indexa desde el archivo
(como `--force`), pero corre las validaciones de un track normal antes de tocar el índice:
round-trip, ruido estructural, frontmatter no declarado y reglas `on_write`. Un archivo inválido
falla con el error de validación y no modifica el índice; `--force` conserva su comportamiento de
saltar el round-trip; `--reindex` + `--force` se rechaza con un mensaje claro. Sobre un documento
no trackeado se comporta como track (incluido fallar si el archivo no valida).

Además comprobé a mano, con un store temporal y el CLI real:
- `docs track --reindex login.md` sobre un archivo editado y válido actualiza el documento;
- un archivo inválido es rechazado y los bytes de todo `.sldb` (incluido `store.yaml`) quedan iguales;
- `--reindex --force` termina con `--reindex and --force cannot be combined: ...`;
- `--force` sigue aceptando el archivo inválido.

## Pruebas ejecutadas

| Comando | Resultado |
|---|---|
| `pytest -q tests/api/test_api_documents.py` | 21 passed, rc 0 |
| `pytest -q tests/api/test_on_write_entering.py` | 7 passed, rc 0 |
| `pytest -q tests/test_links_batch_cli.py` | 5 passed, rc 0 |
| `pytest -q tests/test_clean_code_rules.py` | 1212 passed, rc 0 |
| `pytest -q tests/test_cli_v2.py tests/test_cli_every_command_has_a_handler.py tests/test_cli_format_coverage.py` | 55 passed, rc 0 |
| `bash tools/check.sh --fast` | rc 0, todas las puertas pasan |
| `python -m sldb selfdoc check` | rc 0, `ok: true` |

Entorno: el `/tmp/ws-venv` indicado no existe en este host; usé el venv del repo,
`/workspace/sldb/.venv` (Python 3.13.18), con `TMPDIR=/tmp`. La salida completa está en
`validation.log`.

PASA

# Veredicto

El commit del ejecutor `389868dc8ff40f87c7700175ed1f76f15cf22fc6` ("undo_changes: guard de contenido sin procedencia y steps=N atómico", con `Task-Id` de la tarea) cumple el encargo y pasa la validación del tester.

## Qué se verificó

- Guard stale de undo: el inverso usa `expected_content_hash` (`document_content_hash`: texto del documento sin el bloque de procedencia) y `check_guards` lo compara contra el contenido actual. Un cambio ajeno seguido de la vuelta al contenido anterior ya no da `stale`.
- `steps=N` atómico: `UndoStack.undo_changes` encadena los N inversos con `api.apply_batches`, en una transacción y un cerrojo; cada paso se prevalida contra el estado que deja el anterior. La pila solo se recorta después de aplicar la cadena entera. En un rechazo responde `applied: False`, `written: False`, `undone: 0`, `remaining` intacto y no cambia ningún archivo.
- Contrato documentado: docstring de `undo_changes`, `docs/architecture/mcp.md` (Undo) y `CHANGELOG.md` describen "mismo contenido salvo procedencia" y el todo o nada de `steps=N`.
- `expected_source_hash` y el formato de procedencia no cambian para los demás llamadores.

## Pruebas

Entorno: el `.venv` del checkout tiene `bin/python` como symlink roto a `/home/robocop`; usé el Python 3.13 del host con el `site-packages` del `.venv` por `PYTHONPATH`. No es un problema del cambio.

- `tests/mcp/test_write_tools.py`: **14 passed, 1 xfailed**. Incluye los tres tests nuevos de undo y los tests previos de undo/stale.
- `tests/mcp` completo: **59 passed, 1 xfailed**.
- Tests de módulos tocados/relacionados, de a uno, todos OK:
  - `tests/api/test_transaction.py`: 15 passed
  - `tests/api/test_apply_batch_lock.py`: 4 passed
  - `tests/api/test_write_paths_validate.py`: 5 passed
  - `tests/api/test_on_write_entering.py`: 7 passed
  - `tests/api/test_api_store_fingerprint.py`: 3 passed
  - `tests/api/test_migration_hash_names.py`: 2 passed
  - `tests/store/test_contract_in_model_node.py`: 13 passed
  - `tests/store/test_diagnostics.py`: 16 passed
  - `tests/store/test_export_contract_frozen.py`: 4 passed
  - `tests/store/test_migration_hash_names.py`: 3 passed
  - `tests/store/test_stale_shard_hashes.py`: 3 passed
  - `tests/mcp/test_extension.py`: 8 passed
  - `tests/mcp/test_mutability.py`: 7 passed
  - `tests/mcp/test_signals.py`: 10 passed

## Antes/después

Contra el árbol del commit padre (`389868dc^`) con el `tests/mcp/test_write_tools.py` nuevo:
- `test_undo_of_a_document_that_went_back_to_the_content_the_batch_left_is_not_stale`: **FALLA** (daba `stale`).
- `test_undo_of_several_is_whole_or_nothing`: **FALLA** (`written: True`, `undone: 1` en vez de nada).
- `test_undo_of_a_chain_over_the_same_document_applies_step_by_step`: pasaba también con el código viejo; es cobertura adicional, no uno de los dos tests exigidos.

Con el commit: los tres pasan.

## Notas

- No corrí la suite completa (`pytest -n 4` / `sldb selfdoc check`): queda para integrate, como indica el encargo.
- El ejecutor reportó que no pudo enviar la nota a IR (`deskops message send --to IR` falló); eso queda pendiente para el coordinador, no afecta al código ni a esta validación.

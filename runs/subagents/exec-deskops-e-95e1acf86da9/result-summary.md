# Result
- Guard de contenido: `src/sldb/api/documents/content_hash.py` (hash del texto sin bloque sldb); `check_guards` acepta `expected_content_hash`; el inverso (`batch_inverse._undo`) lo usa en vez de expected_source_hash.
- `apply_batches` (apply_batch.py, exportado en sldb.api): cadena de lotes en una transacción y un cerrojo, cada uno prevalidado contra el estado del anterior.
- `UndoStack.undo_changes` encadena los N inversos con apply_batches: todo o nada, pila intacta si rechaza.
- Docs: docs/architecture/mcp.md, CHANGELOG.md, docstrings.
- Tests: tests/mcp/test_write_tools.py (3 nuevos, el viejo "stops at first" reemplazado por el atómico). Validación en validation.log. La suite completa la corre integrate.
- Archivos: CHANGELOG.md docs/architecture/mcp.md src/sldb/api/__init__.py src/sldb/api/documents/{apply_batch,batch_inverse,batch_prevalidate,batch_report,content_hash}.py src/sldb/mcp/write/undo.py tests/mcp/test_write_tools.py
- run_id/session: no aplica (ejecutor Scion sin sesión hija registrada).
- Hallazgo: `deskops message send --to IR` falló ("Repository id 'IR' not found in registry"); la nota a IR NO se envió, la debe enviar el coordinador con el sha del commit. El primer `git commit` falló por falta de identidad; se rehízo con `-c user.name/-c user.email` por comando. `deskops advance task` corrió antes del commit (task ahora en ritual-testing).

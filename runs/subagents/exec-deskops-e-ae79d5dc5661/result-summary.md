# Result
Guarda nueva `refuse_lossy_overwrite` (src/sldb/api/documents/lossy_overwrite.py) llamada al inicio de `save_document_payload`: aplica refuse_structural_noise y refuse_undeclared_frontmatter al texto actual del archivo; SLDBValidationError antes de escribir. apply_batch update pasa por ahí. Sin modo force. Nueva en archivo aparte por la regla de 80 líneas.
Files: src/sldb/api/documents/lossy_overwrite.py, src/sldb/api/documents/payload_save.py, tests/api/test_structural_noise.py, tests/api/test_transaction.py, CHANGELOG.md
Validation: ver validation.log (1263 passed; check.sh --fast rc 0).
Pendiente: aviso a deskops y graph_ui (lo hace el coordinador).

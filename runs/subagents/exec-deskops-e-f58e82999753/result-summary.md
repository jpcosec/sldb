# Result
Un documento sin la clave de un campo nuevo con default ahora toma el default al extraer y sigue valido.
- Cause: extraction returns None for an absent key; the model then rejected None for `int`.
- Fix: `src/sldb/runtime/validation.py` `Validator.extract` drops None values for non-required fields (`_without_absent_defaults`).
- Test: `tests/test_campo_con_default.py` (store with model, field added afterwards, no store/doc-invalid, espera_segundos == 4).
- Validation: see validation.log (all rc 0).
- Files committed: src/sldb/runtime/validation.py, tests/test_campo_con_default.py (branch deskops/deskops-e-f58e82999753)
- run_id / session / session_sha256: not available to this agent.

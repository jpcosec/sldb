# Result
run_id: exec-deskops-e-891c1b240153
session: n/a (claude session, no child session file)
session_sha256: n/a

POST /save (batch) 422 por SLDBValidationError causado por pydantic ValidationError ahora incluye
`details` = cause.errors(include_url=False, include_context=False, include_input=False) (JSON-safe: loc, msg, type),
ademas de `ok` y `error`.

Archivos (worktree .worktrees/deskops-e-891c1b240153, rama deskops/deskops-e-891c1b240153):
- src/sldb/cli/serve/save_routes.py (validation_body)
- tests/test_serve_save_422.py (nuevo; usa SimpleBook con title=123, campo str, no int: el modelo fixture existente)

Revisar: se omiten ctx/input/url de errors() para que sea serializable; si se quiere errors() literal, ajustar.
Validacion: ver validation.log.

# Resultado
Rama deskops/deskops-e-05461eadbe5b, commit de código hecho (sin Task-Id, por la aclaración de la revisión; el prompt genérico lo pedía).
- resolve_documents(strict=True por defecto, sin cambio para quien lo llama) devuelve `gaps` [{id, model}]; con strict=False los documentos sin glifo van a gaps.
- resolve_view y evaluate_projection_view: `strict: bool = False`; strict=True conserva el ViewError / el {error} de hoy. ViewError no cambia. Sin huecos, gaps = [].
- evaluate_projection_view: gaps en la raíz del resultado y en notation.gaps.
- sldb serve: GET /notations/view y /views/projection/evaluate (GET y POST) aceptan ?strict=true y devuelven gaps.
## Archivos
src/sldb/api/notations/{node_view,projection_style,projection_view,resolve_documents,resolve_view}.py
src/sldb/cli/serve/{notations_payloads,views_payloads}.py
tests/test_view_reports_unmatched_documents.py
## A revisar
- Modo estricto de proyección: hoy no lanza, devuelve notation.error; se conservó así.
- tests/mcp/test_read_tools.py::test_composed_and_projection_views falla por falta de anyio en el venv (ajeno).
Validación: ver validation.log.
## Bloqueo
`deskops advance task` falla: regla rule-activation-task-code exige recibos preflight/bundle aceptados e intactos; el ReviewDoc ...-bundle-1 tiene anchor_state "changed". No es del código; lo debe resolver el supervisor.

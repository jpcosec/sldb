PASA

# Tester deskops-t-bc5c42713572: documento sin glifo como hueco

Task: `task-resolver-una-vista-informa-como-hueco-el-documento-que-ningun-glifo-casa-en-vez-de-fallar-la-vista-e`
Commit revisado: `3407e6647115a74faa0e7b61177544fefca88475` — `feat: una vista informa como hueco el documento que ningún glifo casa`
Archivos del commit: `src/sldb/api/notations/{node_view,projection_style,projection_view,resolve_documents,resolve_view}.py`, `src/sldb/cli/serve/{notations_payloads,views_payloads}.py`, `tests/test_view_reports_unmatched_documents.py`.

## Veredicto

**PASA.** Una vista ya se resuelve con los documentos que casan y lista los demás en `gaps` como `[{id, model}]`; sin huecos `gaps` es `[]`. `resolve_view` y `evaluate_projection_view` aceptan `strict: bool = False`; con `strict=True` se conserva el `ViewError` de hoy (mismo tipo y mensaje) y `ViewError` no cambió. La ruta de `sldb serve` que evalúa vistas devuelve `gaps` y acepta `strict` por query param (GET y POST), y `/notations/view` también. `sldb notations validate` no se tocó.

## Validación ejecutada (detalle en validation.log)

Se corrieron de a un archivo, con `TMPDIR=/tmp` y `--basetemp=/tmp/pytest-deskops-t-bc5c42713572`:

| Comando | rc | Resultado |
|---|---|---|
| `pytest -q tests/test_view_reports_unmatched_documents.py` | 0 | 6 passed |
| `pytest -q tests/notations/test_notation_view_and_routes.py` | 0 | 9 passed |
| `pytest -q tests/notations/test_ported_from_spec2viz_notation_view.py` | 0 | 11 passed |
| `pytest -q tests/notations/test_ported_from_spec2viz_catalog_resolved_views.py` | 0 | 1 passed |
| `pytest -q tests/notations/test_ported_from_spec2viz_view_contract_resolved.py` | 0 | 8 passed |
| `pytest -q tests/notations/test_ported_from_spec2viz_style_palette.py` | 0 | 29 passed |
| `pytest -q tests/notations/test_notations_validate_cli.py` | 0 | 11 passed |
| `pytest -q tests/segments/test_field_transclusion_and_diagram_segments.py` | 0 | 5 passed |
| `bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |

No existe `tests/test_<modulo>.py` para ninguno de los módulos tocados; por eso se corrieron además los tests existentes de notación, vistas y segmentos que ejercitan esos caminos. No se corrió la suite completa.

## Revisión del cambio

- **Huecos:** `resolve_documents(..., strict=False)` separa con `_split_gaps` los documentos que casan de los que no, y devuelve `gaps: [{id, model}]` con el nombre del modelo del documento (p. ej. `SpecDoc`). `strict` sigue siendo el modo por defecto de `resolve_documents`, así que su contrato previo no cambia; las funciones de vista son las que estrenan `strict=False`.
- **`resolve_view`:** propaga `strict` y devuelve `gaps` (vacío sin huecos). En modo estricto levanta el mismo `ViewError` de siempre.
- **`evaluate_projection_view`:** siempre incluye `gaps` (vacío sin notación o sin huecos). Con `strict=True` el bloque `notation` conserva el `{error: "no glyph..."}` de hoy; `result["nodes"]` sigue siendo la selección de la vista y `notation.nodes` solo los documentos dibujados, con los no casados aparte en `gaps`.
- **`sldb serve`:** GET y POST de `/views/projection/evaluate` leen `strict` de la query y `/notations/view` también; `1/true/yes` activan el modo estricto.
- **Commit:** sin trailer `Task-Id`, como pedía el encargo.

## Observaciones no bloqueantes

- `docs/architecture/notations-and-views.md` (§5.1-5.2) aún documenta las firmas sin `gaps` ni `strict`; el encargo no pedía tocar documentación y las puertas rápidas no la comprueban.
- Extra fuera del veredicto: `tests/mcp/test_read_tools.py` no arranca en este entorno por `ModuleNotFoundError: No module named 'anyio'` (dependencia ausente del venv local, ajena al commit).
- Entorno: `/tmp/ws-venv` no existe en este host; usé el venv del proyecto `/workspace/sldb/.venv` (Python 3.13.18), con el que `tools/check.sh --fast` pasa.

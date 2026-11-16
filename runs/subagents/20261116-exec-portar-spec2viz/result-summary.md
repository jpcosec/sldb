# Resultado: task-portar-a-sldb-las-pruebas-de-spec2viz-de-notaciones-paletas-vista-resuelta-y-viewdoc

Ejecutor: deskops-e-aedd8fa5525a (rol sldb-executor). Resultado: **LISTO, rc 0**. Pills atados: ninguno (`pills: []`), así que no hubo choques entre pill y contrato.

## Qué cambió

Un archivo nuevo por cada archivo de spec2viz, importando solo sldb (`sldb.api`, `sldb.api.notations`, `sldb.notations`, `sldb.cli.main`):

| Origen (spec2viz/tests) | Archivo portado (tests/notations) | Casos (contando parametrizados) | No portado |
|---|---|---|---|
| test_notation.py | test_ported_from_spec2viz_notation.py | 28 | parte `notation validate` de test_cli_list_and_validate (se porta como `test_cli_list`); salida de texto y `--strict` de test_cli_notation_sync (se comprueba el JSON) |
| test_notation_view.py | test_ported_from_spec2viz_notation_view.py | 11 | rama `else` de `relation_doc_has_attributes()` (sldb < 0.1.11, no aplica) |
| test_style_palette.py | test_ported_from_spec2viz_style_palette.py | 29 | partes CLI `notation validate` / `palette validate`; los 2 tests de Mermaid/PlantUML (renderers de specIR) |
| test_catalog_notation.py | test_ported_from_spec2viz_catalog_notation.py | 8 | ninguno |
| test_catalog_resolved_views.py | test_ported_from_spec2viz_catalog_resolved_views.py | 1 | los 8 casos (`view_to_mermaid` y `catalog build` son de specIR); se agrega un caso con la parte de vista resuelta del primero |
| test_view_contract_resolved.py | test_ported_from_spec2viz_view_contract_resolved.py | 8 | ninguno |
| test_view_doc.py | test_ported_from_spec2viz_view_doc.py | 6 | ninguno |

Total: 91 casos, todos pasan. No hay xfail, así que no mandé notas al inbox.

Equivalencias de símbolos que usé:
- `spec2viz.notation` → `sldb.notations`
- `spec2viz.palette` → `sldb.notations`
- `spec2viz.styling` → `sldb.notations`
- `spec2viz.exceptions` → `sldb.notations.exceptions`
- `spec2viz.notation_view` → `sldb.api.notations`
- `spec2viz.sldb_sync` (`NotationSync`, `SpecSync`, `sync_catalog`, `resolve_spec_notation`) → `sldb.api.notations`
- `spec2viz.loader.load` y `validator.validate` → `sldb.api.notations.load_spec` y `validate_spec`
- `spec2viz.sldb_models.ViewDoc` → `sldb.api.ViewDoc`

Equivalencias de comandos de la CLI:

| spec2viz | sldb |
|---|---|
| `notation list` | `sldb notations list` (JSON) |
| `notation sync N` | `sldb notations sync --notation N` (JSON) |
| `palette sync` | `sldb notations sync --palette` |
| `notation view` | `sldb notations view` |
| `catalog sync --config X` | `sldb notations sync --catalog X` |
| `catalog validate` | `sldb notations sync --catalog X --check` |
| `diagram sync S --notation N` | `sldb notations sync --spec S --notation N` |

Fixtures:
- Las de `spec2viz/tests/fixtures` que usan estos tests ya estaban en `tests/fixtures/specs/` y son idénticas byte a byte (lo comprobé con `cmp`): component.kinds, component.styled, deployment.nested, deployment.runtime, activity.lanes, class.packages y matrix.quotation-view. Las uso desde ahí y no las dupliqué.
- Los specs del repo de spec2viz se copian con su nombre y su ruta relativa original a `tests/notations/fixtures/docs/architecture/`: `vistas.yml` y `spec2viz/*.yml`, 11 archivos.

CHANGELOG.md: una línea nueva bajo "## 0.1.13 — not released yet", con el mismo estilo que las entradas vecinas.

## Done When
- Los archivos `tests/notations/test_ported_from_spec2viz_*.py` existen (7) y pasan: 91 passed, rc 0.
- No hay xfail, así que no correspondía ninguna nota al inbox.
- No importan spec2viz: el grep negado da rc 0.
- El docstring de cada archivo lista los casos no portados con su motivo, o dice "ninguno".
- El commit lo hace el coordinador con `deskops closeout commit`; yo no hice commit ni push.

## Comandos corridos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/ -k ported_from_spec2viz` → 91 passed, 167 deselected, **rc 0**.
- `! grep -rn 'import spec2viz\|from spec2viz' tests/notations/test_ported_from_spec2viz_*.py` → **rc 0**.
- Además corrí cada archivo por separado mientras lo portaba; todos dieron rc 0.

## Archivos tocados
- tests/notations/test_ported_from_spec2viz_notation.py (nuevo)
- tests/notations/test_ported_from_spec2viz_notation_view.py (nuevo)
- tests/notations/test_ported_from_spec2viz_style_palette.py (nuevo)
- tests/notations/test_ported_from_spec2viz_catalog_notation.py (nuevo)
- tests/notations/test_ported_from_spec2viz_catalog_resolved_views.py (nuevo)
- tests/notations/test_ported_from_spec2viz_view_contract_resolved.py (nuevo)
- tests/notations/test_ported_from_spec2viz_view_doc.py (nuevo)
- tests/notations/fixtures/docs/architecture/vistas.yml (copia)
- tests/notations/fixtures/docs/architecture/spec2viz/*.yml (11 copias)
- CHANGELOG.md (1 línea)
- runs/subagents/20261116-exec-portar-spec2viz/{validation.log,result-summary.md}

No toqué `src/`, `desk/`, `.sldb/` ni los cambios ajenos. Los tests corrieron con esos cambios ajenos presentes en el árbol y no les afectaron.

## Desvíos y dudas
1. **Mensajes de error.** El mensaje de `diagram_type` inválido en sldb es "is not a valid diagram type", no "not a spec2viz diagram type". La aserción exige solo "diagram type".
2. **Errores de la CLI.** Los errores de `sldb notations sync --notation`/`view` salen como `SystemExit(mensaje)`, no como exit 1 con texto; se prueban con `pytest.raises(SystemExit, match=...)`. Los errores tipados de `--catalog`/`--check` salen por stderr, no por stdout.
3. **Builtins y DiagramType.** `test_builtins_load_and_cover_every_diagram_type` usa el `DiagramType` de sldb, que también incluye `reflection`, y pasa.
4. **Informe extra del catálogo.** En `test_every_catalog_spec_resolves_under_its_builtin_notation` salto los informes cuyo `spec_id` empieza por "catalog ". Es el informe de reconciliación del catálogo que solo emite sldb, como se ve en `test_notations_sync_spec_cli.py`.
5. **Caso agregado.** `test_catalog_resolved_views` no tenía ningún caso aplicable. Para que el archivo no quedara vacío agregué un caso que comprueba solo la vista resuelta que consumía `view_to_mermaid`; no es un port literal y lo digo en su docstring.
6. **Ubicación de las fixtures.** No copié a `tests/notations/fixtures/` las fixtures que ya estaban idénticas en `tests/fixtures/specs/`. La Precisión dice "fixtures copiadas van a tests/notations/fixtures"; como estas no hacía falta copiarlas, las uso desde donde ya estaban.

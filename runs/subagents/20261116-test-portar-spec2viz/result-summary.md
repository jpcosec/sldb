# Tester deskops-t-ba1b1f54d370: task-portar-a-sldb-las-pruebas-de-spec2viz-de-notaciones-paletas-vista-resuelta-y-viewdoc

Veredicto global: **PASA**. La salida completa está en `validation.log`, en esta misma carpeta.

Entorno: `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev` funcionó sin error. `uv.lock` ya tenía cambios ajenos antes de que yo empezara, y `--frozen` no lo tocó. `spec2viz` no se puede importar en ese venv (`ModuleNotFoundError`).

## Validation

| Comando | Resultado | Veredicto |
|---|---|---|
| `TMPDIR=/dev/shm pytest -q tests/notations/ -k ported_from_spec2viz` | 91 passed, 167 deselected, 0 xfail, 0 skip, rc 0 (65 s) | PASA |
| `! grep -rn 'import spec2viz\|from spec2viz' tests/notations/test_ported_from_spec2viz_*.py` | sin coincidencias, rc 0 | PASA |

## Done When, punto por punto

1. **Existen los 7 archivos `test_ported_from_spec2viz_<nombre>.py`, uno por archivo de origen**: PASA. Los nombres siguen la convención de la Precisión.
2. **Pasan, con xfail solo donde se mandó nota**: PASA. No hay ningún `xfail` ni `skip` en los archivos (lo comprobé con grep), así que no hacía falta ninguna nota al inbox.
3. **No importan spec2viz**: PASA. El grep da vacío. Revisé además todos los imports y solo salen `sldb.*`, `pytest`, `yaml` y la stdlib. Ningún archivo apunta fuera del repo (no hay `../spec2viz` ni `SLDB_1`), y los tests corren en un venv donde spec2viz no se puede importar.
4. **El docstring lista los casos no portados con su motivo**: PASA. Comparé los nombres de los `def test_*` de origen con los portados:
   - notation 14/14: `test_cli_list_and_validate` pasa a llamarse `test_cli_list`, y el docstring explica que la parte de `validate` queda fuera.
   - notation_view 11/11.
   - style_palette 14/16: faltan los 2 tests de Mermaid/PlantUML, y el docstring da el motivo (son de specIR).
   - catalog_notation 6/6.
   - catalog_resolved_views 1/8: el docstring lista los 8 casos con su motivo (renderer o `catalog build`, de specIR) y explica que el caso agregado no es un port literal.
   - view_contract_resolved 2/2.
   - view_doc 3/3.

   Comprobé el motivo "sldb no tiene `notations validate`": `sldb notations --help` solo ofrece `list, sync, view, resolve, from-graph`.
5. **Commit**: no aplica al tester. Lo hace el coordinador con `deskops closeout commit`.

## Fixtures

- Las 12 copias de `tests/notations/fixtures/docs/architecture/` (`vistas.yml` y 11 `spec2viz/*.yml`) son idénticas a las de spec2viz según `cmp`. Son exactamente los 11 specs que referencia `vistas.yml`, aunque spec2viz tenga 23 archivos en esa carpeta.
- Las 7 fixtures que el ejecutor reutiliza de `tests/fixtures/specs/` son idénticas byte a byte a las de `spec2viz/tests/fixtures/`.
- Desvío aceptable: el ejecutor no duplicó esas 7. La Precisión habla de las fixtures "copiadas", y estas no lo son.

## Casos que el ejecutor no cubrió (`/dev/shm/tester-ba1b/edge.py`, 3 passed)

- **`test_skip_catalog_hides_no_spec`**: el test del catálogo entero salta los informes cuyo `spec_id` empieza por `"catalog "`. Quería ver si eso podía esconder specs, porque el original solo exige `len(reports) >= 9`. Con `sync_catalog` salen exactamente 11 informes de spec, todos distintos y todos con `skipped == []`. Además salen **0** informes `"catalog "`, así que esa rama de skip nunca se ejecuta por esta vía. Es inocua, pero contradice el punto 4 de "Desvíos" del ejecutor, que dice que sldb emite ese informe. No es un fallo, solo una observación.
- **`test_missing_spec_in_catalog_is_an_error`** (caso negativo): si borro un spec que `vistas.yml` referencia, `sync_catalog` lanza `UnknownReferenceError` en vez de saltarlo en silencio. Por tanto la copia incompleta de fixtures no podría pasar desapercibida.
- **`test_no_spec2viz_importable`**: confirma que el venv no puede importar spec2viz.

## Alcance (no se tocó nada fuera del contrato)

- Los cambios del ejecutor son los 7 `tests/notations/test_ported_from_spec2viz_*.py`, `tests/notations/fixtures/` y `CHANGELOG.md` (+1 línea en la línea 7, debajo de `## 0.1.13 — not released yet` de la línea 5, en español y con el estilo de las entradas vecinas). Además está su carpeta de run.
- No hay cambios suyos en `src/` ni en `desk/`.
- Ajenos que no cuentan: `apply_batch.py`, `lock.py`, `tests/api/test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/` y `.herdr-coordination.md`.
- `.sldb/` (`RunDoc.yaml`, `store_index.yaml`, `store.yaml` y los dos `RunDoc/run-deskops-*.yaml`) solo registra los RunDoc del ejecutor y de este tester. Viene del despacho del coordinador, no de cambios del ejecutor.

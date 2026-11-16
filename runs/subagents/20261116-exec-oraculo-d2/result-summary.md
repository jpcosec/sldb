# Resultado: executor deskops-e-4b91d6885d4e

Task: `task-el-oráculo-de-paridad-de-d2-deja-de-importar-spec2viz-golden-congelado-en-tests-notations`. Pills: ninguno (sin conflictos que anotar).

## Cambios
- `tests/notations/goldens/component_spec_python_spec2viz.json` (nuevo, y carpeta `goldens/` nueva): salida de `spec2viz.generators.python_ast.generate_python_ast_spec` sobre una copia de `TREE` escrita en `/dev/shm`, normalizada con la forma de `_defined`: claves `modules`, `classes`, `defines` (lista ordenada de pares `[from, to]`) y `_source` = `91ba1d0ccc14716c7ad63538a1757639ab9e8c94` (`git -C /mnt/ssd/proyectos/SLDB_1/spec2viz rev-parse HEAD`). JSON con `sort_keys=True, indent=2`.
  - Generación: spec2viz no está instalado; se usó `PYTHONPATH=/mnt/ssd/proyectos/SLDB_1/spec2viz TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python gen_golden.py <golden>` (script copiado en este run-dir, `gen_golden.py`; lee `TREE` del archivo de test con `ast`). Con el python3 del sistema falló por falta de pydantic, por eso el entorno de uv. Tras generar, `_source` se recortó a la salida exacta de `rev-parse HEAD` (el script le añadía prefijo y nombre de la función).
- `tests/notations/test_component_spec_python.py`:
  - `test_matches_spec2viz_on_modules_classes_and_defines`: quitado `pytest.importorskip("spec2viz.generators.python_ast")`; lee el golden (`SPEC2VIZ_GOLDEN`, constante nueva de módulo) y compara `_defined(spec)` convertido a `{"modules", "classes", "defines": sorted(list pares)}` contra esas tres claves del golden. Resto de asserts intactos.
  - Docstring del módulo actualizado; imports `json` y `pathlib.Path`.
- `CHANGELOG.md`: una línea en español bajo `## 0.1.13 — not released yet`.

La paridad coincidió con el golden sin tocar `component_spec_from_python`.

## Done When
- Test pasa sin spec2viz importable: `python -c "import spec2viz"` en el entorno de la suite (uv) da `ModuleNotFoundError` (rc=1) y el archivo pasa 5/5 sin skips (`-rs` no lista ninguno).
- El grep de Validation no encuentra imports de spec2viz (`! grep ...` rc=0).
- Golden y CHANGELOG listos para commit (lo hace el coordinador con closeout).

## Comandos (detalle en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q -rs tests/notations/test_component_spec_python.py` → rc=0 (5 passed)
- `! grep -n 'import.*spec2viz\|importorskip("spec2viz' tests/notations/test_component_spec_python.py` → rc=0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev python -c "import spec2viz"` → rc=1 (esperado)

## Archivos tocados
- tests/notations/test_component_spec_python.py
- tests/notations/goldens/component_spec_python_spec2viz.json (nuevo)
- CHANGELOG.md
- runs/subagents/20261116-exec-oraculo-d2/{validation.log,result-summary.md,gen_golden.py}

## Desvíos / dudas
- Primera corrida del grep falló (rc=1) porque mi docstring decía "never imports spec2viz", que casa con `import.*spec2viz`; reformulado y re-corrido (log final limpio).
- `uv.lock` ya estaba modificado antes (cambio ajeno); no lo toqué.

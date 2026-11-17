# Resultado — executor deskops-e-55d271007190 (regresión de B2 en component_spec_from_python)

## Cambios
- `src/sldb/api/notations/component_spec_python.py`
  - nueva `_python_facts(root)`: `find_files(root)` filtrado a `.py`, cada uno con `scan_file(rel, root, ids)` en un mismo `Ids`, y después `ids.flush(...)`. Es `scan_tree` restringido a Python (antes de B2 `scan_tree` solo leía `.py`).
  - `component_spec_from_python` usa `_python_facts` en lugar de `scan_tree`; los imports pasan de `scan_tree` a `find_files`, `Ids` y `scan_file`, que son APIs existentes de `sldb.code`. El docstring del módulo explica el límite.
  - `scan_tree`, `find_files` y `scan_file` no se tocaron (siguen igual para `code_facts` y las anclas).
- `tests/notations/test_component_spec_python.py`: nuevo `test_only_python_files_make_the_spec`. Usa el árbol `pkg` del fixture, le agrega `pkg/vendor/production.min.js` (JS minificado que no parsea) y `pkg/util.ts`, y exige que `(spec, findings)` sean iguales a los del árbol sin esos archivos, donde el único hallazgo es el de `pkg/bad.py`.
- `CHANGELOG.md`: entrada en 0.1.13.

## Done When
- Los comandos de Validation pasan con el test nuevo: los 4 con rc=0 (ver validation.log). test_component_spec_python 6 passed, test_component_spec_graph 16 passed, test_clean_code_rules 1201 passed, check.sh --fast: TODAS LAS PUERTAS PASAN.
- Reproducción de la regresión: con el `component_spec_python.py` de HEAD (cargado con `git show HEAD:...`), un árbol con `pkg/a.py` y `pkg/vendor/production.min.js` da `[('component-spec/syntax-error', 'pkg/vendor/production.min.js')]`. Con el cambio da `[]`.
- El spec de src/sldb no cambia respecto de HEAD: se generó con la versión de HEAD y con la nueva sobre `src/sldb` y los dos `(spec, findings)` son idénticos (JSON ordenado). Sin `root_package` son 2555 nodos, 6463 aristas y 0 hallazgos; con `root_package="sldb"` también son idénticos.
- CHANGELOG: hecho. El commit y el aviso a IR no se hicieron, por la prohibición del brief y la indicación del coordinador (no commit, no avisos); quedan para el cierre.

## Comandos (todos con TMPDIR=/dev/shm uv run --frozen --extra code --extra dev)
- pytest -q tests/notations/test_component_spec_python.py → rc=0
- pytest -q tests/notations/test_component_spec_graph.py → rc=0
- pytest -q tests/test_clean_code_rules.py → rc=0
- bash tools/check.sh --fast → rc=0
- python <scratchpad>/cmp.py (comparación HEAD contra nuevo, ad hoc) → rc=0
No se corrió la suite completa ni `sldb stores build --check` (no figuran en Validation; quedan para el integrador).

## Archivos tocados
- src/sldb/api/notations/component_spec_python.py
- tests/notations/test_component_spec_python.py
- CHANGELOG.md
- runs/subagents/20261116-exec-b2reg/validation.log, result-summary.md (entrega)

Los cambios en `.sldb/` que muestra `git diff` ya estaban en el árbol antes de empezar y no son míos.

## Desvíos o dudas
- Ninguno. No hay pills. `uv` funcionó, así que no hizo falta el fallback a `uvx`.

## REFORMULACION

Propósito: que el spec de componentes generado desde Python no pierda dependencias reales que hoy quedan invisibles (imports dentro de `def`, `class`, `if`, `try`, `with`, incluido `TYPE_CHECKING`). Resultado: una función de recorrido completo en `src/sldb/code/imports.py`; `attrs.nested_imports` en el fact de módulo de `src/sldb/code/scan.py`; aristas `imports` en `component_spec_python.py` también desde `nested_imports`, deduplicadas por par origen/destino; tests en `tests/notations/test_component_spec_python.py` y `tests/selfdoc/test_treesitter_symbols.py`; entrada de CHANGELOG. Repo: `sldb` en `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar `attrs.imports` ni `facts.rels`; no estilos de renderers; no oráculo de paridad con spec2viz; sin push; el commit lo hace el coordinador.

## AMBIGUEDADES

1. "Agregar py_nested_imports(root) que hace un recorrido completo": la firma omite `src`, pero `py_imports(root, src)` necesita los bytes para leer nombres. Obliga a inventar si la nueva función recibe también `src` o si `root` lo encapsula.
2. "guardar esos imports en un attr aparte attrs.nested_imports": no declara el formato; obliga a asumir si replica exactamente las cadenas de `attrs.imports` (p. ej. `"os,sys"` para `import os, sys`).
3. "deduplicadas contra las de nivel superior": no fija si la deduplicación ocurre antes o después de resolver relativos en `_imports`; obliga a inventar el punto del pipeline.
4. "un aviso con deskops message send --to <repo>": `<repo>` no se concreta; obliga a inventar el identificador del repo.

## DRY-RUN

Lecturas: `src/sldb/code/imports.py`, `src/sldb/code/scan.py`, `src/sldb/api/notations/component_spec_python.py`, ambos tests, `CHANGELOG.md`. Cambios previstos: `py_nested_imports` (recorrido total, excluye hijos directos del nodo module); cálculo y guardado de `attrs["nested_imports"]` en `_module_fact`; unión deduplicada en `_module_elements`/`_imports`; caso `pkg/lazy.py` en `TREE`; aserciones de `nested_imports` e `imports` intacto; línea de CHANGELOG. Dependencias: extra `[code]` (tree-sitter-python). Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py` y `TMPDIR=/dev/shm pytest -q tests/selfdoc/test_treesitter_symbols.py`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y el aviso (o lo anota en `runs/subagents/<run-dir>/result-summary.md` si el repo no está registrado); no hay push. Un humano o nodo revisor confirma que la paridad con spec2viz (tarea golden aparte) y el estilo de renderers quedan fuera.

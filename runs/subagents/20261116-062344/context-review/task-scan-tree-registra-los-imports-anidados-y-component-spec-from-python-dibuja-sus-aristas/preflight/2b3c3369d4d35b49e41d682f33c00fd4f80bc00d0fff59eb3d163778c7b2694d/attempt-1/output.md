REFORMULACION
Propósito: que el spec de componentes generado desde Python incluya los imports anidados como aristas `imports`. Resultado: `py_nested_imports` recorre todo el árbol; `scan.py` guarda `attrs.nested_imports` sin tocar `attrs.imports` ni `facts.rels`; `component_spec_python.py` une imports superiores y anidados, deduplicando por par origen-destino; tests y CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: no cambiar renderers, `facts.rels` ni paridad con spec2viz; no push; commit del coordinador; requiere extra `[code]`.

AMBIGUEDADES
1. «agregar al dict TREE un módulo "pkg/lazy.py"… ("module_pkg_lazy", "module_json")»: no dice si `module_json` ya existe en `TREE` ni cómo representarlo; obligaría a inventar su nodo/entrada o asumir una fixture no citada.
2. «una función que recorre el árbol completo y devuelve los imports anidados»: no fija formato de retorno ni si replica exactamente el de `py_imports`; obligaría a inventar tipo y estructura.
3. «deduplicadas contra las de nivel superior»: no define la clave si hay alias o imports relativos; obligaría a inventar si se deduplica por módulo resuelto, texto o alias.

DRY-RUN
Lecturas: `src/sldb/code/imports.py` (`py_imports`), `src/sldb/code/scan.py` 50-70, `src/sldb/api/notations/component_spec_python.py` (`_module_elements`, `_imports`), ambos tests y `CHANGELOG.md`. Cambios previstos: añadir `py_nested_imports(root)` excluyendo hijos directos del módulo; guardar `attrs["nested_imports"]`; unir y deduplicar aristas en el spec; añadir casos de test y entrada de changelog. Dependencias: tree-sitter-python instalado, fixtures existentes, HEAD orientativo. Validaciones futuras: ejecutar los dos `pytest` indicados; comprobar nuevas aristas, inmovilidad de `attrs.imports`, changelog y commit con los archivos de Files. Sin ejecutar nada.

FUTURO
El ejecutor produce código, tests, changelog y `runs/subagents/<run-dir>/result-summary.md`. El coordinador hace `deskops closeout commit` sin push; un humano o nodo revisor acepta el resultado. Si se envía aviso, `deskops message send --to <repo>` o la línea alternativa en el informe.

**REFORMULACION**

El nodo es una tarea de código ejecutable en el repo SLDB_1. Persigue que `component_spec_from_python` incluya una arista `imports` por cada import anidado —dentro de `def`, `class`, `if`, `try` o `with`— además de los de nivel superior, sin alterar `attrs.imports` ni los `facts.rels` existentes. El resultado esperado: una función de recorrido completo en `src/sldb/code/imports.py`, un attr aparte `attrs.nested_imports` en `src/sldb/code/scan.py`, aristas deduplicadas por par origen/destino resuelto en `src/sldb/api/notations/component_spec_python.py`, tests nuevos en los dos archivos indicados y una línea en `CHANGELOG.md`. Límites: no cambiar `facts.rels`, no marcar estilos en renderers, no tocar el oráculo de paridad con spec2viz; el commit y el cierre los hace el coordinador.

**AMBIGUEDADES**

1. Firma de la función nueva. El contrato dice: «Agregar py_nested_imports(root) que hace un recorrido completo», mientras la pill dice: «py_nested_imports(root, src) recibe los mismos argumentos que py_imports(root, src)». Obliga a inventar si `src` es parámetro y si se usa para extraer nombres; el ejecutor tendría que elegir entre contrato y pill.

**DRY-RUN**

Lecturas: `src/sldb/code/imports.py`, `src/sldb/code/scan.py`, `src/sldb/api/notations/component_spec_python.py`, los dos tests nombrados, `CHANGELOG.md`, la pill y el átomo. Cambios previstos: añadir `py_nested_imports` con recorrido completo del árbol, excluyendo los hijos directos del módulo y devolviendo el mismo formato que `py_imports`; guardar `attrs["nested_imports"]` en `_module_fact`; en `_module_elements` unir `imports` y `nested_imports`, resolver relativos y deduplicar por par ya resuelto; añadir al `TREE` el módulo `pkg/lazy.py` y comprobar las dos aristas pedidas; verificar que `attrs.imports` no cambia; añadir la entrada de changelog. Dependencias: extra `[code]` con tree-sitter-python y fixtures/helpers existentes. Validaciones futuras, sin ejecutar: `TMPDIR=/dev/shm pytest -q tests/notations/test_component_spec_python.py` y `TMPDIR=/dev/shm pytest -q tests/selfdoc/test_treesitter_symbols.py`.

**FUTURO**

El ejecutor produce `runs/subagents/<run-dir>/result-summary.md` y el aviso al repo; el coordinador ejecuta `deskops closeout commit` con el mensaje del título y no hace push. Si el código real contradice la pill, el ejecutor se detiene y lo reporta; la decisión de corregir contrato o pill es humana.

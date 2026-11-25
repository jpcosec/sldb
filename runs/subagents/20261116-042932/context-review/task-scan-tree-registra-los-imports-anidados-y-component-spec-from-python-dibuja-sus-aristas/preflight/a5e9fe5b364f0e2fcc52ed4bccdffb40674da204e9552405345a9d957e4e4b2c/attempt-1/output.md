## REFORMULACION

Encargo: hacer que el spec de componentes generado desde Python (`component_spec_from_python`) incluya aristas `imports` también para imports anidados (dentro de `def`, `class`, `if`, `try`, `with`), que hoy se pierden porque `scan_tree` solo registra sentencias de nivel superior. Resultado esperado: `py_nested_imports(root)` en `src/sldb/code/imports.py`; `attrs.nested_imports` en `scan.py`; unión deduplicada de `attrs.imports` + `attrs.nested_imports` al emitir aristas en `component_spec_python.py`; tests nuevos en `tests/notations/test_component_spec_python.py` y `tests/selfdoc/test_treesitter_symbols.py`; entrada en `CHANGELOG.md`. Repo: SLDB_1. Límites: no cambian `attrs.imports` ni `facts.rels`, no hay estilo distinto en renderers, y el oráculo de paridad con spec2viz queda fuera.

## AMBIGUEDADES

1. "deduplicadas contra las de nivel superior" — no dice la clave: ¿módulo, módulo+alias, sentencia? Obliga a inventar el criterio de igualdad.
2. "una arista imports por cada import anidado" — si el mismo módulo se importa dentro de dos funciones, ¿una arista o dos? Obliga a decidir cardinalidad.
3. "excluye los nodos hijos directos del módulo" — no aclara cómo tratar un `import` dentro de `if TYPE_CHECKING` a nivel de módulo (es hijo indirecto) frente a otros anidamientos; el ejemplo lo sugiere, pero la regla textual no lo fija.
4. "en src/sldb/code/scan.py (líneas 58-61...)" y demás números de línea — pueden no coincidir con el checkout; no obliga a inventar, pero sí a localizar por contenido.

## DRY-RUN

Lecturas: `imports.py` (`py_imports`), `scan.py` 50-70, `component_spec_python.py` (`_module_elements`, `_imports`), los dos tests y `CHANGELOG.md`. Cambios previstos: nueva función de recorrido completo; guardado de `attrs["nested_imports"]`; unión deduplicada en las aristas; casos de test (import en función, bajo `TYPE_CHECKING`; `attrs.imports` invariante); changelog. Dependencias: extra `[code]` (`tree-sitter-python`). Validaciones futuras: los dos `pytest` listados y commit con los archivos de `files`.

## FUTURO

El oráculo de paridad con spec2viz (golden congelado) lo resuelve otra tarea. La decisión sobre estilo visual de estas aristas corresponde a un nodo de renderers. La revisión y aceptación del commit es de un humano/JP.

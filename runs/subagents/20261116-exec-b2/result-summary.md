# Resultado — executor deskops-e-640c751d7c12, task B2 (parte TS)

Task: `task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2`. Pills atados: ninguno.
Aclaraciones del coordinador aplicadas: (1) uv.lock es de esta tarea (relock encima del previo), (2) nodos JSX válidos: jsx_element, jsx_self_closing_element y fragmentos, en cualquier punto, también en funciones anidadas, (3) un export default sin nombre toma el último segmento del módulo, (4) con varios `/** */` cuenta el último, y debe cerrar en la línea anterior a la declaración, su export o su decorador, (5) signature, imports y recorded_with con la forma de Python, (6) apply_batch y lock ya commiteados, (7) los avisos a IR los manda el coordinador.

## Cambios (archivo → función)
- `pyproject.toml`: extra `code` + `tree-sitter-typescript>=0.23`. `uv lock` (sin --frozen) una vez → añade tree-sitter-typescript 0.23.2. El lock también conserva el relock previo de los extras code y mcp (añade truststore, uvicorn, etc.).
- `src/sldb/code/runtime.py`: `GRAMMARS` (por extensión), `TS_SUFFIXES`, `grammar_of(path)`, y un `_RUNTIME` que pasa a ser un dict por gramática. `runtime(path=".py")`, `available(path=".py")` y `parse(src, path=".py")` eligen la gramática: `.ts` → typescript; `.tsx`, `.js` y `.jsx` → tsx. Si falta la gramática, `TreeSitterUnavailable` nombra el extra `[code]`.
- `src/sldb/code/files.py` (nuevo): `find_files` sale de scan.py. Incluye `.ts/.tsx/.js/.jsx` solo si `available(".ts")`. Ahora también salta `node_modules` (ver desvíos).
- `src/sldb/code/scan.py`: `scan_file` despacha `.ts/.tsx/.js/.jsx` a `lang_ts.scan_ts_file`. Saqué `_analysis` (captures, owners y names) para dejar `scan_file` en 10 líneas o menos. La ruta de Python no cambia de comportamiento.
- `src/sldb/code/lang_ts.py` (nuevo): `scan_ts_file`, `_module_fact`, `_definition_fact`.
- `src/sldb/code/ts_readers.py` (nuevo): `function_of`, `declarations`, `kind_of`, `has_jsx`, `jsdoc`, `ts_signature`, `ts_imports`.
- `src/sldb/code/ts_fingerprints.py` (nuevo): `ts_fingerprints`, `body_of`, `signature_text`. Reutiliza `_sha` y `_tokens` de `fingerprints.py` (no los duplica). `NORMALIZATION` sigue en 1.
- `src/sldb/models/code_ref.py`: `SUFFIXES`. `parse_code_ref` acepta `.py/.ts/.tsx/.js/.jsx`.
- `src/sldb/api/anchors/record_anchor.py`: `recorded_with(path=".py")`. Para `.py` no cambia (`treesitter-symbols/1 (tree-sitter-python X)`). Para TS/JS da `treesitter-symbols/1 (tree-sitter-typescript 0.23.2, tsx|typescript)`. `record_anchor` le pasa la ruta.
- `tests/fixtures/treesitter/frontend/src/{App.tsx, useToggle.ts, util.js, Panel.jsx}` (nuevos). Cubren: componente, hook, interface, type, función, componente con memo y fragmento, default export anónimo, reexport, función anidada, dos JSDoc seguidos y JSDoc separado por una línea en blanco.
- `tests/selfdoc/test_treesitter_symbols.py`: `_RUNTIME` pasa a `{}` en el test existente, y hay 4 tests nuevos (kinds, doc/signature/span/imports, types solo en .ts/.tsx más el sufijo `~2` con a.js/a.ts, y que sin la gramática TS se siga escaneando .py).
- `tests/api/test_anchors.py`: 3 tests nuevos (ancla .tsx intact/changed/reconnected/lost, ancla .js intact, recorded_with de .py intacto y parse_code_ref de las 4 extensiones).
- `CHANGELOG.md`: entrada en 0.1.13.

## Done When
- Comandos de Validation: los 7 dan rc=0 (ver validation.log).
- Ancla `code:src/Card.tsx::Card`: intact; changed(body) al cambiar el JSX; reconnected a `::Tile` al renombrarla; lost al borrarla (`test_a_tsx_component_anchor_is_intact_changed_reconnected_and_lost`).
- Ancla `code:src/util.js::double`: se registra y queda intact (`test_a_js_function_anchor_records_and_stays_intact`). Uso un util.js en tmp, igual al del fixture.
- Sin tree-sitter-typescript se sigue escaneando .py (`test_without_the_ts_grammar_python_still_scans`).
- La salida de los .py no cambia: `NORMALIZATION` sigue en 1, la ruta de Python solo se reorganizó (`_analysis`), y test_fingerprints, test_treesitter_agreement, test_component_spec_python y los tests de Python existentes pasan sin tocarlos.
- CHANGELOG: hecho. **Commit: no**, porque el brief lo prohíbe y queda para el integrador o coordinador. **Aviso a IR: no**, porque lo manda el coordinador (aclaración 7).

## Comandos (rc)
- `uv lock` → 0
- pytest tests/api/test_anchors.py → 0 (10 passed)
- pytest tests/selfdoc/test_treesitter_symbols.py → 0 (9 passed)
- pytest tests/selfdoc/test_fingerprints.py → 0 (4 passed)
- pytest tests/selfdoc/test_treesitter_agreement.py → 0 (2 passed)
- pytest tests/notations/test_component_spec_python.py → 0 (5 passed)
- pytest tests/test_clean_code_rules.py → 0 (1177 passed)
- bash tools/check.sh --fast → 0 (TODAS LAS PUERTAS PASAN)
- Extra, fuera de Validation: pytest tests/test_store_seams.py → 0 (2 passed)
- No corrí la suite completa ni `sldb stores build --check` (delegados al integrador; Validation no los nombra).

## Archivos tocados
pyproject.toml, uv.lock, CHANGELOG.md, src/sldb/code/runtime.py, src/sldb/code/scan.py, src/sldb/models/code_ref.py, src/sldb/api/anchors/record_anchor.py, tests/api/test_anchors.py, tests/selfdoc/test_treesitter_symbols.py.
Nuevos: src/sldb/code/files.py, src/sldb/code/lang_ts.py, src/sldb/code/ts_readers.py, src/sldb/code/ts_fingerprints.py, tests/fixtures/treesitter/frontend/src/App.tsx, tests/fixtures/treesitter/frontend/src/useToggle.ts, tests/fixtures/treesitter/frontend/src/util.js, tests/fixtures/treesitter/frontend/src/Panel.jsx.
Más este directorio de entrega (validation.log, result-summary.md).

## Desvíos y dudas
- **Módulos en vez de uno solo**: el Implementation Path pide un único `lang_ts.py` con la query, los readers y los imports. Por la regla de 80 líneas efectivas lo partí en `lang_ts.py` (scan), `ts_readers.py` (readers e imports) y `ts_fingerprints.py`. Además `find_files` pasó a `files.py` para liberar líneas en scan.py, como anticipa el contrato. No uso una query de tree-sitter: recorro los hijos directos de `program`, que es exactamente "solo nivel superior".
- **qualified_name**: sigue a Python. El hecho del símbolo lleva `qualified_name = nombre` y el id es `módulo.nombre` (en Python, `qualified_name` es `K.m` y el id lleva el módulo). La referencia es `code:<ruta>::<nombre>`. El contrato dice "el de un símbolo es módulo.nombre": eso se cumple en el id.
- **Sufijo `~n` de módulos**: lo da `Ids` con un espacio de ids compartido en `scan_tree` y orden por ruta (a.js → `a`, a.ts → `a~2`). En `scan_file` aislado (el que usa record_anchor) cada archivo es su propio espacio, igual que en Python.
- **node_modules**: `find_files` ya no lo recorre. No lo pide el contrato, pero sin esto la reconexión por proyecto (`scan_tree(root)`) en un repo de frontend escanearía todas las dependencias. Solo afecta a .py que estén dentro de un `node_modules`. Si el coordinador no lo quiere, basta quitarlo de `_SKIP` en files.py.
- **Fuera de las reglas**: `nested_imports` de TS es siempre `[]` (no leo `import()` dinámico ni `require`), el doc del módulo TS es `None`, y las clases de TS/JS no crean hechos (las reglas no las nombran).
- **Signature**: de los parámetros solo colapso espacios y re-entrecomillo como `py_norm`. Un default sale `b: number = 1`, no `b: number=1` como en el `ast.unparse` de Python.
- **Bug corregido en el camino**: `os.path.splitext(".tsx")` no da extensión. Lo arreglé en `grammar_of` para aceptar tanto `.tsx` suelto como una ruta.

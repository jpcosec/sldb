# Executor deskops-e-ad176f583599 — facts genéricos de TS/TSX/JS/JSX (C3 de IR para IR09)

Resultado: LISTO 0. Sin commit ni avisos, por la decisión (6) del coordinador.

## Cambios
- `src/sldb/code/ts_calls.py` (nuevo, autorizado por la Precisión): `body_nodes(fn)` recorre el cuerpo en orden de fuente sin entrar en `function_declaration`, `generator_function_declaration`, `class_declaration` ni `class` anidados (las arrows y function expressions sí se recorren, como `lambda` en Python). También `callee(call)`, el texto completo de la expresión llamada vía `py_norm`; `first_arg(call)`, el valor de un string o template sin `${}`, sin delimitadores, o None; y `body_calls(nodes)`, que da `[{name, line, first_arg}]`.
- `src/sldb/code/ts_jsx.py` (nuevo): `jsx_handlers(nodes)` da `[{element, attribute, handler}]` para los `jsx_attribute` cuyo nombre empieza por `on` y cuyo valor es `{identificador}`, `{llamada}` o una función cuyo cuerpo es una llamada (cuerpo expresión, o bloque cuya primera sentencia es una llamada). En ese último caso el handler es el callee interno, según la decisión (3). `element` es `field_text(parent, "name")`, el tag tal como está escrito.
- `src/sldb/code/lang_ts.py`: `_definition_fact` calcula el kind una sola vez y agrega `_extras`. `_extras(kind, fn, src)` da las relaciones `calls` (un destino por llamada o handler distinto, ordenadas como en Python), `attrs.calls` en function, hook y component, y `attrs.handlers` solo en component. Un type no recibe nada nuevo. El docstring está actualizado.
- `tests/fixtures/treesitter/frontend/src/PostForm.tsx` (nuevo, lo autoriza el Implementation Path): un componente con fetch y axios (URLs literales y un template con `${}`), una función anidada `local` que no se recorre, `onClick={handleSave}`, `onChange={() => validate(id)}`, `onBlur={track("blur")}`, `onFocus={props.onFocus}` (no es handler) y `Form.Item`.
- `tests/selfdoc/test_treesitter_symbols.py`: se ajustó una aserción existente porque `Button` ahora lleva `calls -> inner`. Se agregaron dos tests:
  - `test_ts_component_calls_fetch_and_axios_with_their_literal_url_and_its_handlers` (por `sldb.api.code.code_facts`, decisión (5));
  - `test_ts_calls_of_hooks_and_arrows_handlers_in_blocks_and_types_without_calls`.
- `CHANGELOG.md`: una entrada en 0.1.13.

## Done When
- **Validation pasa:** los 5 comandos dan rc=0 (ver `validation.log`).
- **Fetch y axios con su URL literal:** `src.PostForm.PostForm.attrs.calls` trae `fetch` con `first_arg: /api/posts` (línea 10), `axios.get` con `/api/posts` (11) y `axios.delete` con `null` (template con `${id}`).
- **La llamada del componente a su handler:** está la relación `{"type": "calls", "target": "handleSave"}`.
- **El handler onClick:** `attrs.handlers[0] == {element: button, attribute: onClick, handler: handleSave}`.
- **Anclas TS sin cambio de estado:** `tests/api/test_anchors.py` pasa (23). Además comparé `scan_tree` contra una copia de HEAD (`git archive` en /dev/shm) sobre `tests/fixtures/treesitter` (182 facts) y `src` (7661 facts): los ids son los mismos y no falta ni sobra ninguno. Solo cambian 11 facts TS, y solo porque se agregan relaciones y atributos; ids, spans, huellas, signature y doc son idénticos. Ningún fact .py o SQL cambia (decisión (4)). `NORMALIZATION` sigue en 1.
- **CHANGELOG:** hecho. **Commit y aviso a IR:** no se hicieron, por la decisión (6) del coordinador.

## Comandos (rc)
1. `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` da rc=0 (47 passed).
2. `... pytest -q tests/api/test_anchors.py` da rc=0 (23 passed).
3. `... pytest -q tests/selfdoc/test_fingerprints.py` da rc=0 (4 passed).
4. `... pytest -q tests/test_clean_code_rules.py` da rc=0 (1203 passed).
5. `... bash tools/check.sh --fast` da rc=0 (TODAS LAS PUERTAS PASAN; omite afirmaciones, pruebas y selfdoc).
6. Extra: `... python3 tools/check_claims.py` da rc=1, con 11 afirmaciones falsas que ya existían. Todas son `docs/missing`, `docs/ambiguous` o `sldb query`, en docs/architecture/*.md y en entradas viejas del CHANGELOG. Ninguna viene de la entrada nueva (el diff del CHANGELOG no nombra `docs/missing`). No las toqué.

No corrí la suite completa ni `sldb stores build --check`.

## Archivos tocados
- `src/sldb/code/lang_ts.py`
- `src/sldb/code/ts_calls.py` (nuevo)
- `src/sldb/code/ts_jsx.py` (nuevo)
- `tests/selfdoc/test_treesitter_symbols.py`
- `tests/fixtures/treesitter/frontend/src/PostForm.tsx` (nuevo)
- `CHANGELOG.md`
- `runs/subagents/20261116-exec-k4/validation.log` y `result-summary.md` (entrega)

## Desvíos y dudas
- **Clave de las llamadas:** el Scope dice `{func, line, first_arg}`. La Precisión y la decisión (1) del coordinador piden la forma exacta de Python, que es `{name, line}`, así que uso `{name, line, first_arg}`.
- **Funciones anidadas:** no entro en declaraciones anidadas con nombre (`function`, `class`), igual que con `def` y `class` en Python. Las arrows y function expressions sí se recorren, como `lambda` en Python. Consecuencia: `const h = () => fetch(...)` dentro de un componente aporta sus llamadas al componente, y `function h() { fetch(...) }` anidada no las aporta (los facts TS son solo de nivel superior).
- **Handlers:** según el contrato, solo valen identificador o llamada. Por eso `onFocus={props.onFocus}` (member expression) no es handler. Si IR09 lo necesita, sería una ampliación.
- **Prefijo `on`:** se toma literal, así que un atributo como `only={x}` contaría como handler.
- **`new X()`:** no cuenta como llamada.
- **`first_arg`:** conserva los escapes tal como están escritos (`"a\"b"` da `a\"b`).
- **Árbol compartido:** no toqué ni stageé archivos ajenos, ni `desk/` ni `.sldb/`.

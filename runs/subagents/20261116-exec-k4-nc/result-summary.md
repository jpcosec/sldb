# Ejecutor deskops-e-c92b7022cf97: C3 TS con la decisión del supervisor (canonical: false)

**Resultado: LISTO 0.** No hice commit ni mandé el aviso a IR, por instrucción del coordinador.

## Punto de partida
- Apliqué `git apply --exclude=CHANGELOG.md runs/subagents/20261116-exec-k4-c2/executor-diff-c3ts-c2.patch` sobre un árbol limpio en `src/`, `tests/` y `CHANGELOG.md`.
- El CHANGELOG del patch no aplicaba porque HEAD sumó entradas después. Reescribí la entrada a mano.

## Cambios
- **`src/sldb/code/ts_callee.py`.** `call_name(node, src)` ahora devuelve `(name, canonical)`.
  - `_root` baja por la cadena: objeto de un miembro o de un índice, función de una llamada, y atraviesa `await`, paréntesis, `as`, `satisfies`, `x<T>` y `!`.
  - Si la raíz es un identificador, `this`, `super` o una función, el nombre es canónico. Lo arma `_canonical`, con la tabla de c2, y lleva `canonical: true`.
  - Si la raíz es otra cosa (array, binario, `new`, literal, regex, `import`, etc.), el nombre sale de `loose_text` y lleva `canonical: false`.
  - Se quitaron el builder de `new` (antes `new Foo().bar` daba `Foo().bar`) y la caída al "texto sin espacios".
- **Nuevo `src/sldb/code/ts_loose.py`, `loose_text`.** Es un módulo nuevo del paquete `sldb.code`, autorizado por el Scope.
  - Toma el texto fuente de la expresión llamada y le quita por rangos del árbol:
    - cada palabra `await` con su espacio;
    - los `type_arguments` de un call, un `new` o un `x<T>` (no los de una anotación de tipo).
  - Colapsa cada tramo de espacios en blanco a un solo espacio. Lo hace también dentro de los literales, porque así lo dice la decisión.
- **`src/sldb/code/ts_calls.py`.**
  - `callee` devuelve la tupla.
  - `body_calls` arma cada ítem con `_call` como `{name, line, first_arg, canonical}`.
  - Actualicé el docstring.
- **`src/sldb/code/ts_jsx.py`.** `_handler` toma `callee(...)[0]`. Agregué una línea al docstring.
- **`src/sldb/code/lang_ts.py`, `_extras`.**
  - Las relaciones `calls` salen solo de los nombres canónicos.
  - Un handler cuyo nombre coincide con el de una llamada no canónica no da relación. Un handler que es una llamada siempre aparece también en `attrs.calls`, porque la arrow o el valor se recorren. Uno que es identificador siempre es canónico.
  - Los handlers mantienen la forma `{element, attribute, handler}`.
- **`tests/selfdoc/test_treesitter_symbols.py`.**
  - Los ítems esperados llevan ahora `"canonical": True`.
  - `new Foo().bar` pasa a ser `new Foo().bar` con `canonical: false`.
  - Ningún destino lleva `new`.
  - Test nuevo `test_ts_chains_from_new_binary_literal_or_array_are_not_canonical_and_give_no_relation`. Cubre:
    - `new Set<string>(xs).has` da `new Set(xs).has`, sin type args;
    - `(a  ??\n   []).map` da `(a ?? []).map`, con los espacios colapsados;
    - `'a b'.split` da `'a b'.split`;
    - `[...x].sort` da `[...x].sort`;
    - `(await [y]).at` da `([y]).at`, sin await.
    - Los cinco llevan `canonical: false`. La única relación `calls` es `ok`.
    - Un handler `{() => [z].forEach(f)}` aparece en `handlers`, pero no da relación.
- **`CHANGELOG.md`.** La entrada de la tarea en 0.1.13 describe `canonical`, el texto colapsado de los no canónicos, que estos no dan relación y `ts_loose.py`.
- **Sin cambios respecto de c2:** el fixture `PostForm.tsx`.

## Medición en los tres frontends reales (solo lectura; `probe.py` en este directorio, salida al final de `validation.log`)
- Forma canónica comprobada con la regex: `^(ident|\(fn\))(\??\.ident|\(\)|\??\.?\[\]|!)*$`.

| Árbol | Facts | Llamadas | Canónicas (distintas) | No canónicas (distintas) | Canónicas fuera de forma | No canónicas con espacios dobles, await o salto de línea | Destinos `calls` | Destinos fuera de forma o no canónicos |
|---|---|---|---|---|---|---|---|---|
| UIs/graph_ui/apps/knowledge-workbench/src | 179 | 460 | 450 (226) | 10 (10) | 0 | 0 | 360 | 0 |
| sldb/surface/src | 752 | 3361 | 3249 (1433) | 112 (105) | 0 | 0 | 2268 | 0 |
| UIs/marcado-ui/src | 120 | 461 | 447 (221) | 14 (14) | 0 | 0 | 325 | 0 |

- Ninguna llamada quedó sin la clave `canonical`.
- Ningún nombre no canónico contiene `<` ni `await`.
- Ejemplos de no canónicos: `new Date().toISOString`, `[...source.anchored].sort`, `(exported.ranges ?? []).map`, `/\s/.test`, `[...nodes] .sort` (el salto de línea antes de `.sort` queda como un espacio, no se borra) e `import` (un `import('./x')` dinámico).
- Los no canónicos pueden ser largos: el máximo mide 370 caracteres en surface, porque llevan el texto completo de la cadena con sus arrows. Es lo que pide la decisión. Canonizarlos queda para la tarea aparte.

## Done When
- **Validation:** los 5 comandos dan rc=0 (`validation.log`):
  - treesitter_symbols: 50 passed;
  - anchors: 23 passed;
  - fingerprints: 4 passed;
  - clean_code_rules: 1206 passed;
  - `check.sh --fast`: TODAS LAS PUERTAS PASAN.
  - No corrí la suite completa ni `sldb stores build --check`. Validation no los nombra y quedan **delegados al integrador**.
- **Fixture:** salen `fetch` y `axios.get` con `/api/posts`, la relación de `PostForm` a `handleSave` y `onClick` en `attrs.handlers`. Lo cubre `test_ts_component_calls_fetch_and_axios_...`.
- **Frontends reales:** todo nombre canónico cumple la forma y todo no canónico lleva `canonical: false`, sin espacios dobles, sin await y sin type args. Ningún destino `calls` es no canónico (ver tabla).
- **Anclas TS sin cambio de estado:** test_anchors pasa. Ids, spans, huellas y signature no cambian; solo se agregan atributos y relaciones.
- **CHANGELOG:** listo. **Commit y aviso a IR:** no se hicieron, por instrucción.

## Archivos tocados
- `src/sldb/code/lang_ts.py` (M)
- `src/sldb/code/ts_callee.py` (nuevo, del patch c2, reescrito)
- `src/sldb/code/ts_calls.py` (nuevo, del patch c2, modificado)
- `src/sldb/code/ts_jsx.py` (nuevo, del patch c2, una línea y el docstring)
- `src/sldb/code/ts_loose.py` (nuevo)
- `tests/fixtures/treesitter/frontend/src/PostForm.tsx` (nuevo, del patch c2)
- `tests/selfdoc/test_treesitter_symbols.py` (M)
- `CHANGELOG.md` (M)
- Entrega: `runs/subagents/20261116-exec-k4-nc/{validation.log,result-summary.md,probe.py}`

## Desvíos o dudas
- **Espacios dentro de los literales.** También se colapsan: `'a  b'.split` da `'a b'.split`. La decisión dice "cada tramo de espacios colapsado"; si se prefiere conservar los literales intactos, es un cambio chico en `ts_loose`.
- **Handlers no canónicos.** No tienen marca `canonical` propia, porque la forma de `handlers` está fijada en `{element, attribute, handler}`. Su llamada sí aparece en `attrs.calls` con `canonical: false`, así que nada se omite en silencio.
- **`import(...)` dinámico.** Sale como `name: "import"` con `canonical: false`, porque `import` no es identificador.

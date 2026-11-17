# Ejecutor deskops-e-ad176f583599-a2: corrección 1 de C3 TS (facts genéricos de TS/TSX/JS/JSX)

**Resultado: LISTO 0.** No hice commit ni mandé avisos, como pide la corrección del coordinador.

Este intento parte del diff del intento 1 que ya estaba en el árbol (lang_ts.py, ts_calls.py, ts_jsx.py, PostForm.tsx, los tests y el CHANGELOG; ver `runs/subagents/20261116-exec-k4/result-summary.md`). Corrige la única FALLA del tester (`runs/subagents/20261116-test-k4/result-summary.md`) y aplica su observación sobre `on`.

## Cambios
- **`src/sldb/code/ts_calls.py`, `callee`:** toma el campo `function` del `call_expression` y, mientras ese campo sea un `await_expression`, baja a su hijo. La gramática TS lee `await get<T>(...)` como una llamada cuya función es `await get`, con `type_arguments` y `arguments` como hermanos. Los `type_arguments` nunca forman parte del campo `function`, así que `get<T>(...)` y `api.get<T>(...)` ya daban `get` y `api.get`; lo verifiqué parseando. Un `(await g)(1)` es un `parenthesized_expression` y no cambia. También actualicé el docstring del módulo.
- **`src/sldb/code/ts_jsx.py`:** agregué `_is_event(name)`: un atributo es evento si su nombre es `on` seguido de una mayúscula. `onClick` es evento; `only` y `on` no lo son. `jsx_handlers` usa `_is_event`. También actualicé el docstring.
- **`tests/selfdoc/test_treesitter_symbols.py`:** test nuevo `test_ts_generic_calls_drop_type_arguments_and_await_and_only_on_uppercase_is_an_event`. Cubre:
  - `await get<Foo>('/x')` da `get` con `/x`;
  - `api.get<T>('/y')` da `api.get`;
  - `` get<T>(`/z`) `` da `get`;
  - `await api.posts.list<P[]>('/p')` da `api.posts.list`;
  - `new Foo('/n')` no cuenta como llamada;
  - las relaciones `calls` quedan sin `await`;
  - en `<i only={x} on={y} onClick={z} />` solo `onClick` es handler.
- **`CHANGELOG.md`:** la entrada de 0.1.13 de esta tarea ahora dice que `name` va sin argumentos de tipo ni `await`, y que un handler es `on` seguido de mayúscula.

## Done When
- **Validation:** los 5 comandos dan rc=0 (ver `validation.log`):
  - `test_treesitter_symbols`: 48 passed;
  - `test_anchors`: 23 passed;
  - `test_fingerprints`: 4 passed;
  - `test_clean_code_rules`: 1203 passed;
  - `check.sh --fast`: TODAS LAS PUERTAS PASAN.
- **fetch y axios con su URL literal, llamada al handler, onClick en `attrs.handlers`:** se cumplen igual que en el intento 1. Los tests del intento 1 siguen pasando sin cambios.
- **Anclas TS sin cambio de estado:** test_anchors pasa. La corrección solo cambia el texto de `name` y el destino de `calls` cuando hay `await` con tipos genéricos, y saca de `handlers` los atributos `on` + minúscula. Los ids, spans y huellas no cambian.
- **Repro del tester:** `/dev/shm/k4t-aw` ahora da `get` (dos veces) y `api.posts.list`, sin `await`.
- **CHANGELOG:** está actualizado. **Commit y aviso a IR:** no se hicieron, por instrucción del coordinador.

## Comandos (rc)
Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`:

| Comando | rc |
|---|---|
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 |
| `pytest -q tests/api/test_anchors.py` | 0 |
| `pytest -q tests/selfdoc/test_fingerprints.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |

No corrí la suite completa ni `sldb stores build --check`: los dejo al integrador.

## Archivos tocados en este intento
- `src/sldb/code/ts_calls.py`
- `src/sldb/code/ts_jsx.py`
- `tests/selfdoc/test_treesitter_symbols.py`
- `CHANGELOG.md`
- `runs/subagents/20261116-exec-k4-c1/validation.log` y `result-summary.md` (entrega)

`lang_ts.py` y `PostForm.tsx` siguen como los dejó el intento 1. No toqué `desk/`, `.sldb/` ni archivos ajenos.

## Desvíos y dudas
- **`on` + mayúscula:** es más estricto que el texto del Scope ("empiezan por on"). Lo pidió el coordinador en la corrección 1.
- **Sigue fuera del alcance:** `onClick={async () => { await save(p); }}` no da handler, porque el contrato solo acepta un identificador o una llamada.

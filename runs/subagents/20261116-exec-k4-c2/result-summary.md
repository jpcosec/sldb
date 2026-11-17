# Ejecutor deskops-e-2964812cac52: corrección 2 de C3 TS (forma canónica del nombre llamado)

**Resultado: LISTO 0.** No hice commit ni mandé avisos, como pide la corrección del coordinador.

Este intento parte del diff de los intentos 1 y c1, que ya estaba en el árbol: lang_ts.py, ts_calls.py, ts_jsx.py, PostForm.tsx, los tests y el CHANGELOG. Corrige la FALLA del tester c1 (`runs/subagents/20261116-test-k4-c1/result-summary.md`): una cadena escrita en varias líneas daba `client .documents`, con espacio. Implementa la forma canónica de las Precisiones de la corrección 2 del Scope.

## Cambios
- **Nuevo `src/sldb/code/ts_callee.py`, `call_name(node, src)`** (un módulo nuevo del paquete `sldb.code`, autorizado por el Scope). Arma el nombre desde el árbol, no desde el texto:
  - `identifier`, `property_identifier`, `this` y `super` dan su texto;
  - `member_expression` une el objeto y la propiedad con `.`, o con `?.` si el árbol tiene `optional_chain`;
  - `non_null_expression` da `x!`;
  - `subscript_expression` da `[]` (`?.[]` si es opcional);
  - un `call_expression` dentro de la cadena da `()` sin argumentos;
  - un `new_expression` dentro de la cadena da `X()`;
  - una arrow, function expression o IIFE da `(fn)`;
  - se atraviesan `await`, los paréntesis, `as`, `satisfies` e `instantiation_expression`. Los argumentos de tipo de una llamada son hermanos del campo `function` y nunca entran.
  - Cualquier otra expresión (un literal, `a ?? []`, un array) da su texto sin espacios en blanco.
  - Las funciones son chicas y despachan por tabla, para cumplir la regla de 10 líneas de lógica.
- **`src/sldb/code/ts_calls.py`:** `callee` ahora devuelve `call_name(function)`. Dejó de usar `py_norm` y el bucle de `await`. Actualicé el docstring.
- **`ts_jsx.py`:** no cambió. Usa `callee`, así que un handler `{() => client\n .save()}` da `client.save`.
- **`tests/selfdoc/test_treesitter_symbols.py`:** test nuevo `test_ts_call_names_are_canonical_from_the_tree_with_no_whitespace`. Cubre:
  - la cadena `client\n .documents()\n .then(cb)` en varias líneas, que da `client.documents().then` y `client.documents`;
  - `a?.b`, `a!.c`, `a?.[]` y `x[].y`;
  - `(await listDocuments(m)).slice`, que da `listDocuments().slice`;
  - `fetch(url).then(...).then`, que da `fetch().then().then`;
  - la IIFE async, que da `(fn)`;
  - `results.filter(...).map`, que da `results.filter().map`;
  - `(x as any).z`, que da `x.z`, y `new Foo().bar`, que da `Foo().bar`;
  - `first_arg` de `a?.b('/opt')`;
  - que ningún destino de una relación tenga espacios ni `await`;
  - un handler JSX escrito en varias líneas.
- **`CHANGELOG.md`:** la entrada de esta tarea en 0.1.13 describe la forma canónica con ejemplos y nombra `ts_callee.py`.

`lang_ts.py`, `ts_jsx.py` y `PostForm.tsx` quedan como los dejaron los intentos anteriores.

## Done When
- **Validation:** los 5 comandos dan rc=0 (ver `validation.log`):
  - `test_treesitter_symbols`: 49 passed;
  - `test_anchors`: 23 passed;
  - `test_fingerprints`: 4 passed;
  - `test_clean_code_rules`: 1204 passed;
  - `check.sh --fast`: TODAS LAS PUERTAS PASAN.
- **fetch y axios con su URL literal, la llamada del componente a `handleSave` y `onClick` en `attrs.handlers`:** el test del fixture PostForm sigue pasando sin cambios.
- **Anclas TS sin cambio de estado:** test_anchors pasa. Solo cambia el texto de `name` y el destino de `calls`; los ids, spans y huellas no cambian.
- **`attrs.calls`:** es una lista de `{name, line, first_arg}`, con la forma de Python más `first_arg`.
- **CHANGELOG:** está actualizado. **Commit y aviso a IR:** no se hicieron, por instrucción del coordinador.

## Sonda sobre los tres frontends reales (solo lectura, `scan_tree`)
El script es `/tmp/claude-1001/-mnt-ssd-proyectos-SLDB-1-sldb/43592da0-3d7a-464a-8ba8-e901a7d6ef8c/scratchpad/probe2.py` y la salida está en `validation.log`. Revisa todos los `attrs.calls[].name`, los destinos de `calls` y los `handlers`:

| Árbol | Facts | Nombres | Con espacios | Con `await` | Con `<T>` |
|---|---|---|---|---|---|
| ../UIs/graph_ui/apps/knowledge-workbench/src | 179 | 862 | 0 | 0 | 0 |
| surface/src | 752 | 5953 | 0 | 0 | 0 |
| ../UIs/marcado-ui/src | 120 | 888 | 0 | 0 | 0 |

Los casos que citó el tester ahora dan:
- `sldb.ts:173`: `listDocuments().slice`;
- `WorkbenchShell.tsx:82`: `client.documents().then().catch`, `client.documents().then` y `client.documents`;
- `WorkbenchShell.tsx:99`: lo mismo, con `client.modelsCatalog`;
- `SourceAnchoringView.tsx:402`: lo mismo, con `client.rank`.

## Comandos (rc)
Todos se corrieron con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`:

| Comando | rc |
|---|---|
| `pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 |
| `pytest -q tests/api/test_anchors.py` | 0 |
| `pytest -q tests/selfdoc/test_fingerprints.py` | 0 |
| `pytest -q tests/test_clean_code_rules.py` | 0 |
| `bash tools/check.sh --fast` | 0 |
| `python probe2.py` (los 3 frontends) | 0 |

No corrí la suite completa ni `sldb stores build --check`: los dejo al integrador.

## Archivos tocados en este intento
- `src/sldb/code/ts_callee.py` (nuevo)
- `src/sldb/code/ts_calls.py`
- `tests/selfdoc/test_treesitter_symbols.py`
- `CHANGELOG.md`
- `runs/subagents/20261116-exec-k4-c2/validation.log` y `result-summary.md` (entrega)

No toqué `desk/`, `.sldb/`, los frontends ni archivos ajenos.

## Desvíos y dudas (decisiones fuera del texto de las Precisiones)
- **`new X()` dentro de una cadena:** se escribe `X()` (`new Date().toISOString` da `Date().toISOString`). Las Precisiones no lo cubren y la forma no puede llevar espacios. `new X()` sola sigue sin ser una llamada.
- **Un objeto que no es nombre ni llamada** (un literal, `a ?? []`, `[a, b]`) da su texto sin espacios en blanco: `body.documents??[].filter().map`, `[severity,code].filter().join`. Un string con espacios como objeto (`"a b".split`) pierde sus espacios internos.
- **`a?.()`:** una llamada opcional directa da `a`. No escribo el `?.` de la llamada misma.
- **Python:** tiene el mismo defecto con las cadenas en varias líneas (`Post.objects .filter`), según el tester c1. Queda fuera del alcance de esta tarea.

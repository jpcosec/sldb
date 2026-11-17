# Tester deskops-t-6db9547051f6: corrección 2 de C3 TS (forma canónica del nombre llamado)

**Veredicto: FALLA.**

Lo que pidió la corrección anterior está arreglado:
- no queda ningún `name` ni destino de `calls` con espacios, `await` ni argumentos de tipo en los tres frontends reales ni en `/dev/shm/k4t-*`;
- las cadenas en varias líneas, `()`, `(fn)` y `[]` salen como dicen las Precisiones.

Pero la sonda (1) también exige la forma canónica de las Precisiones de corrección 2: el nombre "se arma desde el árbol, no desde el texto", y un tramo de la cadena que es una llamada "se escribe con '()' sin sus argumentos". Cuando el objeto de la cadena no es un nombre, una llamada, una función ni un índice (un array, un literal, un regex, un template o un `a ?? b`), `ts_callee.call_name` cae al **texto del nodo sin espacios en blanco** (`ts_callee.py:32`). En los tres frontends reales eso da **129 nombres distintos fuera de la forma canónica**:

| Tipo de nombre | Cuántos | Ejemplo |
|---|---|---|
| Lleva llamadas con sus argumentos | 20 | `[...newSet(data.atoms.flatMap((a)=>a.tags.map((t)=>`${t.split(':')[0]}:`)))].sort` (`knowledge-workbench/src/pages/ComposerView.tsx:36`) |
| Lleva arrows sin `(fn)` | 7 | el mismo ejemplo de arriba |
| Inventa un identificador que no existe | 4 | `new Set(xs)` da `newSet(xs)` (`surface/src/core/atoms.ts:377`) |
| Cambia la lectura de la expresión | 31 | `(exported.ranges ?? []).map` da `exported.ranges??[].map`, que se lee `exported.ranges ?? [].map` (`marcado-ui/src/lib/marcado-runtime.ts:117`) |
| Altera el contenido de un literal | (dentro de los 50 regex/str/template) | `"a b".split` da `"ab".split`; un template con `" "` interno pierde el espacio |

El caso extremo, en `marcado-ui/src/lib/marcado-runtime.ts:146`, es un `name` de unos 300 caracteres. Lleva tres `.map((entry)=>formatDiagnostic(entry.code,...))` completos, con sus argumentos.

El ejecutor lo declaró como desvío ("da su texto sin espacios en blanco"). Contradice el texto explícito de las Precisiones: armar el nombre desde el árbol y escribir `()` sin argumentos y `(fn)`. Por eso, con el mismo criterio que usó c1 con las cadenas en varias líneas, lo clasifico como FALLA. El CHANGELOG afirma la forma canónica "desde el árbol y no desde el texto" y no menciona esta caída al texto.

Una posible corrección, que decide el coordinador: recorrer también los arrays, los binarios y los literales con la misma tabla, o darles un marcador fijo (por ejemplo `[...]`, `(expr)` o `(lit)`).

## Validation (corrida por mí, salida completa en `validation.log`)
| Comando | Resultado |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | PASA (49 passed, rc=0) |
| pytest -q tests/api/test_anchors.py | PASA (23 passed, rc=0) |
| pytest -q tests/selfdoc/test_fingerprints.py | PASA (4 passed, rc=0) |
| pytest -q tests/test_clean_code_rules.py | PASA (1204 passed, rc=0) |
| bash tools/check.sh --fast | PASA ("TODAS LAS PUERTAS PASAN", rc=0) |

`uv run --frozen` funcionó y no hizo falta el fallback a `uvx`. No corrí la suite completa ni `sldb stores build --check`: los dejo al integrador.

## Sondas de la corrección
**(1) Ni espacios, ni `await`, ni argumentos de tipo, y forma canónica: FALLA (por la forma canónica).** El script es `/dev/shm/k4t3-scripts/probe.py`. Revisa `attrs.calls[].name`, los destinos de `calls` y los handlers.

| Árbol | Facts | Distintos | Con espacios | Con `await` | Con `<` | Fuera de la forma canónica |
|---|---|---|---|---|---|---|
| knowledge-workbench/src | 179 | 237 | 0 | 0 | 0 | 8 |
| surface/src | 752 | 1565 | 0 | 0 | 0 | 101 |
| marcado-ui/src | 120 | 268 | 0 | 0 | 0 | 14 |
| /dev/shm/k4t-fe | 4 | 17 | 0 | 0 | 0 | 0 |
| /dev/shm/k4t-aw | 2 | 2 | 0 | 0 | 0 | 0 |

- **Forma canónica (la regex está en `probe.py`):** un identificador o `(fn)`, seguido de tramos `.x`, `?.x`, `()`, `[]`, `?.[]` o `!`.
- **Lo que sí está bien:**
  - las cadenas en varias líneas (`client.documents().then`);
  - `listDocuments().slice`;
  - `fetch().then().then`;
  - `(fn)` para las IIFE;
  - `obj[]`, `a?.b` y `Set().has`.
- **Lo que falla:** el desglose por tipo de nombre está en `noncanon.out`, dentro de `validation.log`.

**(2) `first_arg`: PASA.** Probado en `/dev/shm/k4t3-edge/src/E.tsx`:
- `'/a'`, `"/b"` con opciones y `` `/c` `` dan su valor;
- `` `/d/${u}` ``, un identificador, ninguno argumento y `'/e' + u` dan `null`;
- un comentario antes del literal no molesta (da `/g`);
- los escapes quedan como están escritos, como dice el docstring.

**(3) Handlers `on` + mayúscula: PASA.**
- `onkeyup` no es handler; `onSubmit={go}` sí.
- `svg:rect` y `Form.Item` salen tal como están escritos.
- Un string, un atributo sin valor (`onE`), un ternario o una arrow vacía no son handler.
- Cada handler suma su relación `calls`.

Notas, que no considero fallas porque el Scope dice "identificador o llamada":
- `onClick={this.handleSave}` y `onF={handlers.open}` no son handler;
- `onBlur={async () => await save(1)}` no es handler (`save` sí sale en `calls`);
- `{() => { log(); run(); }}` toma solo `log`.

**(4) Facts existentes contra HEAD: PASA.** Comparé el código de HEAD (`git archive` en `/dev/shm/k4t3-head`, con `sldb.__file__` verificado) con el del árbol, sobre los mismos árboles de entrada:

| Árbol | Facts (HEAD/árbol) | Facts cambiados | Inesperados |
|---|---|---|---|
| tests/fixtures | 182/182 | tsx 8, ts 1, jsx 1, js 1 | 0 |
| src | 7674/7674 | 0 | 0 |
| knowledge-workbench/src | 179/179 | tsx 79, ts 35 | 0 |
| surface/src | 752/752 | tsx 184, ts 270 | 0 |
| marcado-ui/src | 120/120 | tsx 36, ts 38 | 0 |
| /dev/shm/k4t-fe | 4/4 | tsx 3 | 0 |

- Ningún fact `.py` ni SQL cambió (54 facts SQL).
- En los TS solo se agregan relaciones `calls` y `attrs.calls` y `attrs.handlers`.
- Ids, spans, huellas, signature y las demás relaciones quedan iguales.

**(5) La forma es la de Python: PASA.**
- Las llamadas de Python tienen las claves `{name, line}`; las de TS, `{name, line, first_arg}`.
- La relación es `{type: calls, target}` en los dos lenguajes.
- `handlers` es `{element, attribute, handler}`.

## Done When
- **Validation: PASA.**
- **fetch y axios con su URL, la llamada a `handleSave` y `onClick` en `attrs.handlers`: PASA.** Lo cubre el test del fixture PostForm.
- **Anclas TS sin cambio de estado: PASA.** Pasa test_anchors y la sonda (4) no muestra cambios.
- **CHANGELOG: PASA con reparo.** Está la entrada, pero afirma una forma "desde el árbol" que no se cumple para objetos literales.
- **Commit y aviso a IR:** no se hicieron, por instrucción del coordinador. No lo evalúo.

## Regresiones vecinas: PASA
- En `src/` cambiaron `lang_ts.py` y los módulos nuevos `ts_callee.py`, `ts_calls.py` y `ts_jsx.py`.
- `grep -rlE 'lang_ts|ts_calls|ts_jsx|ts_callee' tests` encuentra solo `tests/selfdoc/test_treesitter_symbols.py`, que da 49 passed.

## Fuera del contrato: PASA
- En `src/` y `tests/` solo están `lang_ts.py`, los tres módulos nuevos (autorizados por el Scope), el test, el fixture `PostForm.tsx` y `CHANGELOG.md`.
- `.sldb/`, `desk/` y `runs/` son del coordinador.
- Los archivos ajenos del brief (`apply_batch.py`, `lock.py`, `uv.lock`) no aparecen modificados.

Scripts y salidas en `/dev/shm/k4t3-scripts/`, el borde en `/dev/shm/k4t3-edge/` y la base de HEAD en `/dev/shm/k4t3-head/`. No toqué el repo salvo esta entrega.

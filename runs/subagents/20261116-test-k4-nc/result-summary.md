# Tester deskops-t-ff9633b313a5: C3 TS (canonical: false), intento nc

**Veredicto: PASA.** Hay tres observaciones sin bloqueo (ver al final). Ninguna aparece en los tres frontends reales.

Evidencia completa en `validation.log`. Scripts propios en este directorio: `probe.py` (sonda), `cmp.py` (HEAD contra el árbol) y `Edge.tsx` (casos borde). Se corrieron desde `/dev/shm/k4nc/`, sin editar el repo.

## Validation (corrida por mí, `uv run --frozen --extra code --extra dev`; uv funcionó)
| Comando | Resultado |
|---|---|
| pytest tests/selfdoc/test_treesitter_symbols.py | 50 passed, rc=0 — PASA |
| pytest tests/api/test_anchors.py | 23 passed, rc=0 — PASA |
| pytest tests/selfdoc/test_fingerprints.py | 4 passed, rc=0 — PASA |
| pytest tests/test_clean_code_rules.py | 1206 passed, rc=0 — PASA |
| bash tools/check.sh --fast | TODAS LAS PUERTAS PASAN, rc=0 — PASA |

Validation no nombra la suite completa ni `sldb stores build --check`, así que no los corrí: quedan **delegados al integrador**.

## Done When, punto por punto
- **Fixture — PASA.** Lo comprobé ejecutando el fixture, no solo leyendo el test.
  - `PostForm` lleva `fetch` con `/api/posts` y `axios.get` con `/api/posts`. `axios.delete` con template `${id}` da `first_arg: null`.
  - `attrs.handlers` trae `{button, onClick, handleSave}`, más `Form.Item` con `onChange→validate` y `onBlur→track`.
  - Las relaciones `calls` incluyen `handleSave`.
  - `{props.onFocus}` no es handler.
  - `fetch("/hidden")`, dentro de la función anidada `local`, no se cuenta.
- **Frontends reales (solo lectura, con mi sonda) — PASA.**

  | Árbol | Facts | Llamadas | Canónicas | No canónicas | Malas | Destinos `calls` malos | Handlers |
  |---|---|---|---|---|---|---|---|
  | knowledge-workbench/src | 179 | 460 | 450 | 10 | 0 | 0 | 32 |
  | sldb/surface/src | 752 | 3361 | 3249 | 112 | 0 | 0 | 213 |
  | marcado-ui/src | 120 | 461 | 447 | 14 | 0 | 0 | 88 |

  Qué cuenta como "mala":
  - un canónico fuera de la regex de forma;
  - un no canónico con espacios dobles, salto de línea o tab, `await`, `<…>(`, comentario o espacios en los bordes, o con aspecto canónico;
  - una llamada sin la clave `canonical` o con claves distintas de `{name, line, first_arg, canonical}`.

  Qué cuenta como "destino malo":
  - un destino que sea un nombre no canónico;
  - uno fuera de forma;
  - uno que no salga de un canónico ni de un handler del mismo fact;
  - un handler cuyo atributo no sea `on` seguido de mayúscula.
- **Revisión a mano de 10 no canónicos al azar (seed 17) — PASA.** Los 10 se leen igual que el fuente:
  - `/^\s{6}-\s+type:\s+/.test`
  - `(view?.notation ?? "—").replace`
  - `/^[a-zA-Z0-9][a-zA-Z0-9_-]*$/.test`
  - `(report.warnings ?? []).map`
  - `(current?.fields ?? []).map(similarityQuery).filter`
  - `/\(it\s+"it"…/.exec`
  - `(schema?.enum ?? [value]).map`
  - `(v === undefined ? [] : Array.isArray(v) ? v : [v]).map`
  - `[...new Set(data.atoms.flatMap((a) => a.tags))].sort`
  - `[...hits].sort`

  Ningún no canónico real tiene un literal con doble espacio en su línea (0 candidatos), así que el colapso dentro de literales no alteró ningún dato real.
- **Facts existentes idénticos a HEAD — PASA.**
  - Método: base con `git archive HEAD src` en `/dev/shm/k4nc/head` y `scan_tree` con `PYTHONPATH` en cada lado.
  - Alcance: los 3 frontends, `tests/fixtures/treesitter` y `src/sldb/code`, 1428 facts.
  - Quitando `attrs.calls`, `attrs.handlers` y las relaciones `calls` de los TS, el JSON es byte a byte idéntico (`cmp` rc=0).
  - Los ids, spans, huellas, firmas y los facts de `.py` y SQL no cambian. Las anclas: test_anchors pasa, 23.
- **first_arg — PASA.**
  - string → valor sin comillas, y conserva los espacios internos (`'/a  b'` da `/a  b`);
  - template sin `${}` → valor;
  - template con `${}` → null;
  - escapes tal como están escritos;
  - un tagged template `` sql`select 1` `` da `first_arg: 'select 1'`.
- **Handlers on + mayúscula — PASA.** `onclick`, `only`, `on` y `{a.b}` no son handlers. `onX` sí.
- **CHANGELOG — PASA.** Hay una entrada en 0.1.13 que describe `canonical`, el texto colapsado (también dentro de un literal), que los no canónicos no dan relación y los módulos nuevos.
- **Commit y aviso a IR:** no son del tester. Siguen pendientes, por instrucción del coordinador al ejecutor.

## Alcance de archivos — PASA
Cambios de la tarea:
- `M`: `lang_ts.py`, `test_treesitter_symbols.py` y `CHANGELOG.md`.
- Nuevos: `ts_callee.py`, `ts_calls.py`, `ts_jsx.py`, `ts_loose.py` (módulos nuevos de `sldb.code`, autorizados) y el fixture `PostForm.tsx`.

`ts_readers.py` no se tocó. Los cambios en `.sldb/` y `desk/` son del coordinador. Los cambios ajenos del brief ya no aparecen en `git status`.

## Regresiones vecinas — PASA
- El único módulo de `src/` modificado es `lang_ts.py`. El único test que lo importa por nombre es `test_treesitter_symbols.py`: 50 passed.
- Corrí además los usuarios de `scan_tree` y `code_facts`, cada uno por separado:
  - test_anchors: 23 passed;
  - test_component_spec_python: 6 passed;
  - test_treesitter_agreement: 2 passed.

## Casos borde que el ejecutor no cubrió (`Edge.tsx`; salida en validation.log)
Funcionan bien:
- `a!.c()` da `a!.c`.
- `a[0].b()` da `a[].b`.
- Una IIFE function o arrow da `(fn)`.
- `this.y.z()` da `this.y.z`.
- `new Foo<T>().bar()` da `new Foo().bar`, no canónico.
- `(await [y]).at` da `([y]).at`.
- `import('./m').then(h)` da dos llamadas no canónicas, `import('./m').then` e `import`, ninguna en las relaciones.
- Un handler `{() => new Foo().go()}` aparece en `handlers` sin relación.

Observaciones. Ninguna altera datos de los frontends reales y no las tomo como falla:
1. **Un comentario de línea dentro de un no canónico.** `[1] // comentario\n .map(g)` da `'[1] // comentario .map'`. Al colapsar el salto, el `//` deja `.map` "comentado" y cambia la lectura. Esto no tiene aviso en el resumen ni en el CHANGELOG. En los frontends reales hay 0 casos (la sonda busca `//` y `/*`). Arreglo sugerido: que `ts_loose._dropped` quite los nodos `comment`.
2. **Literales colapsados.** `'a  b'.split` da `'a b'.split` y `/a  b/.test` da `/a b/.test`, lo que cambia el valor del literal. Hay aviso (resumen del ejecutor y CHANGELOG) y sigue la letra de la decisión del supervisor. En los datos reales hay 0 casos.
3. **Huecos de forma menores.**
   - El `?.` de una llamada opcional no queda en el nombre: `a?.()` da `a` y `a.b?.()` da `a.b`. En los frontends reales hay 13 llamadas `?.(`. Es defendible, porque el `?.` es de la llamada y no del nombre, pero en medio de una cadena se perdería (`a?.().b` daría `a().b`).
   - `([] as Array<string>).map` conserva los argumentos de tipo de la anotación `as`. El ejecutor lo declaró: solo quita los type args de una llamada, de un `new` o de `x<T>`.
   - Los handlers no incluyen arrows cuyo cuerpo es `void f()` o `await f()` (`{() => void create()}`, `{async () => { await save(1); }}`). Su llamada sí sale en `attrs.calls`. Hay unas 32 en los frontends reales. El Scope solo exige un identificador o una llamada, así que no es falla.

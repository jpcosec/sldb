# Tester deskops-t-c8ab44d273df-a2: corrección 1 de C3 TS (facts genéricos de TS/TSX/JS/JSX)

**Veredicto: FALLA.** Se arregló el `await` inicial: no queda ningún `name` que empiece con `await`. Tampoco quedan argumentos de tipo en el nombre llamado. Pero la sonda (1) de la corrección exige que ningún `name` ni destino de `calls` tenga espacios, y eso no se cumple. Una llamada encadenada en varias líneas da `name` con espacios:

```ts
client
  .documents()
```

da `"client .documents"` y no `client.documents`. Esto pasa en el cliente HTTP de un frontend real (`surface/src/app/WorkbenchShell.tsx:82`, `:99`, y `workbench/SourceAnchoringView.tsx:402`). Es el mismo tipo de defecto que el de `await`: la URL sale, pero el nombre y el destino de `calls` no son el texto calificado (`client.documents`), y la misma llamada escrita en una línea da otro destino. Ningún test ni el CHANGELOG lo avisan.

Toda la salida está en `validation.log`. Mis scripts están en `/dev/shm/k4t2-scripts/` y la base de HEAD (4bcd1918, sacada con `git archive`) en `/dev/shm/k4t2-head`.

## Validation (corrida por mí)
| Comando | Resultado |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | PASA (48 passed, rc=0) |
| pytest -q tests/api/test_anchors.py | PASA (23 passed, rc=0) |
| pytest -q tests/selfdoc/test_fingerprints.py | PASA (4 passed, rc=0) |
| pytest -q tests/test_clean_code_rules.py | PASA (1203 passed, rc=0) |
| bash tools/check.sh --fast | PASA ("TODAS LAS PUERTAS PASAN", rc=0) |

No corrí la suite completa ni `sldb stores build --check`: los dejo al integrador.

## Done When
- **fetch y axios con su URL literal, la llamada al handler y onClick en `attrs.handlers`: PASA.** Lo cubre el test del fixture PostForm, que pasa.
- **Anclas TS sin cambio de estado: PASA.** test_anchors pasa y la comparación (3) no muestra cambios fuera de lo esperado.
- **CHANGELOG: PASA.** Está la entrada en 0.1.13. Pero no dice nada de las cadenas en varias líneas.
- **Commit y aviso a IR:** no se hicieron, por instrucción del coordinador. No lo evalúo.

## Sondas de la corrección
### (1) Ni `await`, ni argumentos de tipo, ni espacios en `name` o destino de `calls`: FALLA
Cuento las llamadas distintas en `attrs.calls`. La salida completa está en `validation.log`, sección "sondas corrección 1".

| Árbol | Llamadas | `await` inicial | `await` dentro | `<T>` en el nombre llamado | Espacios sin paréntesis (cadena en varias líneas) | Espacios con paréntesis |
|---|---|---|---|---|---|---|
| knowledge-workbench/src | 456 | 0 | 1 | 0 | 6 | 32 |
| surface/src | 3295 | 0 | 2 | 0 | 38 | 190 |
| marcado-ui/src | 457 | 0 | 0 | 0 | 5 | 17 |
| /dev/shm/k4t-fe | 23 | 0 | 1 | 0 | 0 | 2 |
| /dev/shm/k4t-aw (repro anterior) | 3 | 0 | 0 | 0 | 0 | 0 |

- **El defecto anterior está corregido.** Ya no hay `await get` ni `await api.posts.list`; k4t-aw da `get`, `get` y `api.posts.list`. En el único caso que encontré con `<...>` en un nombre (surface, `SourceAnchoringView.tsx:402`), los `<...>` están en la anotación de un parámetro de un callback, dentro del texto de una cadena, no como argumentos de tipo del nombre llamado.
- **FALLA, cadenas en varias líneas.** `py_norm` cambia el salto de línea y la sangría por un espacio. Ejemplos: `client .documents`, `client .modelsCatalog`, `anchors .filter`, `workspaceEntries .filter`, `text .toLowerCase`. Mi repro mínimo está en `/dev/shm/k4t2-edge/src/E.tsx`, líneas 2–4, y da `client .documents` y `client .documents() .then`. Python, ya cerrado, hace lo mismo: `(Post.objects\n .filter(a=1))` da `Post.objects .filter`. TS hereda esa forma vía `py_norm`, pero eso no cumple el criterio (1).
- **Viola el criterio (1) al pie de la letra, aunque cumple la Precisión del contrato** ("texto completo de la expresión llamada"). Cuando lo llamado es a su vez una llamada, una IIFE o algo entre paréntesis, el nombre trae espacios y a veces `await`. Ejemplos:
  - `(await listDocuments(model)).slice`, en `knowledge-workbench/api/sldb.ts:173`;
  - `(async () => { ... await ... })`, en `surface` DistillView:86 y TrayView:66, y en k4t-fe:24;
  - `results.filter((r) => r.model === ...).map`;
  - `fetch(url).then((r) => r.json()).then`.

  Lo dejo para que decida el coordinador. La FALLA se sostiene igual por las cadenas en varias líneas.
- **Bordes que funcionan bien** (`/dev/shm/k4t2-edge`):
  - `a?.b("/opt")` da `a?.b` con /opt;
  - `a!.c('/bang')` da `a!.c`;
  - `api.get<{ id: number }>("/obj")` da `api.get` con /obj.

### (2) `only={x}` ya no es handler: PASA
Lo cubre el test nuevo y lo comprobé por separado en `/dev/shm/k4t2-edge`. En `<div only on once onclick on1 onClick onSubmit>`, solo `onClick` (que da `x`) y `onSubmit` (que da `go`) son handlers.

### (3) Facts existentes contra HEAD (.py, TS, SQL): PASA
Corrí `scan_tree` con el código de HEAD (`PYTHONPATH=/dev/shm/k4t2-head/src`, verifiqué que `sldb.__file__` apuntaba ahí) y con el del árbol, sobre los mismos árboles de entrada:

| Árbol | Facts (HEAD/árbol) | Altas/bajas | Facts cambiados | Cambios inesperados |
|---|---|---|---|---|
| tests/fixtures | 182/182 | 0/0 | tsx 8, jsx 1, ts 1, js 1 | 0 |
| src | 7662/7662 | 0/0 | 0 | 0 |
| knowledge-workbench/src | 179/179 | 0/0 | tsx 79, ts 35 | 0 |
| surface/src | 752/752 | 0/0 | tsx 184, ts 270 | 0 |
| marcado-ui/src | 120/120 | 0/0 | tsx 36, ts 38 | 0 |

- Revisé 7771 facts `.py` y 54 SQL, y ninguno cambió.
- En los TS solo hay relaciones nuevas de tipo `calls` y claves nuevas `attrs.calls` y `attrs.handlers`. Todas las relaciones previas se conservan, y ningún otro campo cambia: ids, spans, huellas y signature quedan iguales.

## Regresiones vecinas: PASA
- En `src/` cambiaron `src/sldb/code/lang_ts.py` y los módulos nuevos sin trackear `ts_calls.py` y `ts_jsx.py`.
- `grep -rlE 'lang_ts|ts_calls|ts_jsx' tests` encuentra solo `tests/selfdoc/test_treesitter_symbols.py`, que da 48 passed.

## Fuera del contrato: PASA
- En `src/` y `tests/` solo están `lang_ts.py`, `ts_calls.py`, `ts_jsx.py` (módulos nuevos autorizados), el test, el fixture `PostForm.tsx` y `CHANGELOG.md`.
- Los cambios en `.sldb/`, `desk/` y `runs/` son del coordinador.
- Los archivos ajenos que nombra el brief (`apply_batch.py`, `lock.py`) hoy no aparecen como modificados.

## Para corregir (sugerencia, no lo implementé)
Armar `name` sin el espacio que dejan los saltos de línea antes de `.` o `?.`. Hay dos formas:
- quitar el espacio en blanco alrededor de `.`/`?.` fuera de los argumentos;
- reconstruir el nombre desde los nodos `member_expression`.

Agregar un test con `client\n  .documents()`. Si Python debe seguir la misma forma, tiene el mismo problema.

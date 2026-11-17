# Tester deskops-t-c8ab44d273df: facts genéricos de TS/TSX/JS/JSX (C3 de IR para IR09)

**Veredicto: FALLA.** En una llamada genérica con `await` (`await get<T>("/x")`), `name` incluye `await`. El error está en código común (clientes HTTP tipados) y no se avisa. El resto pasa.

Toda la salida está en `validation.log`. Los scripts están en `/dev/shm/k4t-scripts/`, la base de HEAD en `/dev/shm/k4t-head` (sacada con `git archive`) y los fixtures de prueba en `/dev/shm/k4t-fe` y `/dev/shm/k4t-aw`.

## Validation (corrida por mí)
| Comando | Resultado |
|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | PASA (47 passed, rc=0) |
| pytest -q tests/api/test_anchors.py | PASA (23 passed, rc=0) |
| pytest -q tests/selfdoc/test_fingerprints.py | PASA (4 passed, rc=0) |
| pytest -q tests/test_clean_code_rules.py | PASA (1203 passed, rc=0) |
| bash tools/check.sh --fast | PASA ("TODAS LAS PUERTAS PASAN", rc=0) |

No corrí la suite completa ni `sldb stores build --check`: los dejo al integrador.

Tamaño de los archivos: ts_calls.py 46 líneas, ts_jsx.py 43 y lang_ts.py 62, todos bajo el límite. clean_code pasa.

## Done When, punto por punto
- **fetch y axios con su URL literal: PASA.** En PostForm salen `fetch` con /api/posts (línea 10), `axios.get` con /api/posts (11) y `axios.delete` con null porque es un template con `${id}`.
- **Llamada del componente a su handler: PASA.** Está la relación `calls -> handleSave`.
- **Handler onClick en attrs.handlers: PASA.** Sale `{button, onClick, handleSave}`.
- **Anclas TS sin cambio de estado: PASA.** test_anchors pasa. Además comparé `scan_tree` de HEAD contra el cambio en cinco árboles: fixtures (182 facts), src (7661), knowledge-workbench (179), surface/src (752) y marcado-ui (120). Los ids son los mismos, sin altas ni bajas. Los únicos cambios son relaciones nuevas de tipo `calls` y las claves nuevas `attrs.calls` y `attrs.handlers`. Hay 0 diferencias en cualquier otro campo y 0 facts .py o SQL cambiados (src: changed 0).
- **CHANGELOG: PASA**, hay una entrada en 0.1.13.
- **Commit y aviso a IR:** no se hicieron, por la decisión (6) del coordinador. Esto no lo evalúo.

## Aclaraciones del coordinador
1. **Archivos sin trackear:** ts_calls.py, ts_jsx.py y PostForm.tsx están sin trackear, y los revisé.
2. **Button `calls -> inner`: PASA.** Es una relación agregada. El fact de HEAD tenía solo `contained-in`; en la comparación, todas las relaciones previas se conservan y la nueva es de tipo `calls`. Ningún otro campo cambia.
3. **Facts existentes contra HEAD: PASA.** Ver el punto de anclas: ids y campos idénticos salvo las relaciones y attrs nuevos.
4. **Frontend real:** IR no tiene .tsx. Usé tres frontends reales del workspace en modo solo lectura (`UIs/graph_ui/apps/knowledge-workbench/src`, `sldb/surface/src`, `UIs/marcado-ui/src`) y armé uno sintético en `/dev/shm/k4t-fe/src/Posts.tsx` (useEffect con fetch, axios.post con objeto, handlers inline y por referencia, callbacks por props). Ahí aparece el **defecto principal**:
   - **`await f<T>(...)` da `name: "await f"`.** El parser de TypeScript toma `await get<T>(...)` como una llamada cuya función es `await get`, y `callee()` toma ese texto tal cual. Repro mínimo en `/dev/shm/k4t-aw/src/api.ts`:
     - `await get<Foo>("/typed")` da `{"name": "await get", "first_arg": "/typed"}` y la relación `calls -> "await get"`;
     - `await get("/plain")` da `get` (correcto);
     - `await api.posts.list<Post[]>("/posts")` da `await api.posts.list`.

     En los frontends reales pasa en el cliente HTTP, que es justo lo que IR09 necesita. Por ejemplo, `knowledge-workbench/src/api/sldb.ts` (líneas 82, 101, 133 y 159, `await get<...>('/models')`) y `surface/src/core/client.ts` (147, 152, 153, 166, 167, 169 y 171, `await request<...>("/graph")`). La URL sale bien, pero el nombre llamado queda mal y la relación `calls` apunta a un destino que no existe. Ningún test ni el CHANGELOG lo avisan. **Esto es la FALLA.**
5. **Forma de Python: PASA.** Python (ad6f8842) da `attrs.calls = [{name, line}]` y una relación `{type: calls, target}` por destino distinto, ordenada. TS da `{name, line, first_arg}` y las mismas relaciones; `first_arg` es la única clave extra y la pide el contrato.

## Bordes probados que no cubrió el ejecutor (en /dev/shm)
Estos funcionan bien:
- un comentario antes del primer argumento (`fetch(/* c */ "/api/ping")` da /api/ping);
- `fetch("a"+"b")` y `fetch()` dan null;
- `new URL("/x")` no cuenta como llamada;
- `axios.post('/api/log', {a:1})` da /api/log;
- un template sin `${}` da su valor;
- un callback por props (`<Posts onSelect={(id) => console.log(id)}/>`) da el handler `console.log`;
- un hook no lleva `handlers`.

Estas son observaciones, no la causa de la FALLA:
- **`only={x}` cuenta como handler `x`.** Toma el prefijo `on` literal. El contrato dice "empiezan por on" y el ejecutor lo declaró, así que no lo cuento como falla. Sugiero exigir `on` seguido de mayúscula. En los tres frontends reales no hubo ningún caso.
- **`onClick={async () => { await save(p); }}` no da handler**, porque la primera sentencia es un `await_expression`. Es un falso negativo, pero queda fuera de lo que pide el contrato (identificador o llamada).
- **El nombre de una IIFE es el texto entero de la función**, por ejemplo `(async () => { await fetch('/iife'); })`. Las cadenas largas dan nombres como `fetch(url).then((r) => r.json()).then`. Es el texto completo de la expresión llamada, como en Python, y es coherente con la Precisión, pero genera destinos `calls` ruidosos: 94 en surface/src.
- `py_norm` convierte las comillas dobles del texto de la expresión llamada en simples (`t("k").x` da `t('k').x`); `first_arg` no pasa por esa conversión.

## Fuera del contrato
Aparte de lo que permite el contrato (lang_ts.py, los módulos nuevos ts_calls.py y ts_jsx.py, el test, el fixture y el CHANGELOG), los únicos cambios son de `.sldb/`, `desk/` y `runs/`. Son del coordinador (otras tareas, el Board y los RunDocs), no del ejecutor. **PASA.**

## Regresiones vecinas
El módulo de `src/` cambiado es `sldb.code.lang_ts`, más los nuevos `ts_calls` y `ts_jsx`. Los tests que los importan por nombre son solo test_treesitter_symbols. Agregué los que llaman a scan_tree o code_facts y corrí cada archivo por separado:
- test_treesitter_symbols: 47 passed;
- test_anchors: 23 passed;
- tests/notations/test_component_spec_python.py: 6 passed;
- tests/selfdoc/test_treesitter_agreement.py: 2 passed.

No hay fallas nuevas, así que no hizo falta correr los tests contra HEAD; para los facts sí comparé contra HEAD, más arriba.

## Para corregir (sugerencia, no implementado)
En `ts_calls.callee`: si el nodo `function` es un `await_expression`, usar su hijo, o en general quitar el `await` cuando el padre es `call_expression` con `type_arguments`. Conviene agregar al fixture un caso `await get<T>("/x")`.

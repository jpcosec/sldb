## REFORMULACION

Encargo en el repo SLDB_1 (paquete `sldb.code`): publicar facts sintácticos genéricos de TS, TSX, JS y JSX, sin interpretar frameworks, para que IR09/specIR los interprete. Resultado: relación `calls` desde cada función, componente o hook hacia cada nombre llamado (`fetch`, `axios.get`, `api.posts.create`, otros símbolos); `attrs.calls` con `{func, line, first_arg}`, donde `first_arg` es el literal sin comillas ni backticks o `null` si es template con expresiones; y `attrs.handlers` en componentes con `{element, attribute, handler}` para atributos JSX `on*` cuyo valor sea identificador o llamada, añadiendo también `calls` hacia el handler. Debe seguir la forma exacta de la tarea hermana de Python para `calls`, `attrs.calls` y `kwargs` cuando aplique. Superficie: `src/sldb/code/lang_ts.py`, `ts_readers.py`, módulos nuevos de `sldb.code` (autorizados), fixture en `tests/fixtures/treesitter/frontend/src/`, `tests/selfdoc/test_treesitter_symbols.py`, `CHANGELOG.md`. Límites: no interpretar REST ni frameworks, no resolver imports, no Python.

## AMBIGUEDADES

1. «si esa ya cerró, seguir su forma exacta» / «sigue su forma exacta para calls, attrs.calls y kwargs cuando aplique»: el input no trae el esquema cerrado de la tarea Python; obligaría a inventar nombres de campos y qué significa `kwargs` en JS.
2. «desde cada función, componente o hook» y «attrs.handlers en componentes»: no define cómo distinguirlos sintácticamente; obligaría a inventar heurísticas (mayúscula inicial, retorno JSX).
3. «cuyo valor es un identificador o una llamada»: no aclara qué texto va en `handler` si es llamada (`handleSave()` vs `handleSave`) ni si arrow functions quedan fuera; obligaría a fijar criterio.
4. «{func, line, first_arg}»: no dice si `line` es la de la llamada, del argumento o del símbolo contenedor; obligaría a elegir.
5. Fixture «tests/fixtures/treesitter/frontend/src/» no figura en `files` y solo se autorizan «readers nuevos»; obligaría a decidir si crear fixtures fuera de `files` es válido.
6. «las anclas TS existentes no cambian de estado»: no define qué es un ancla ni cómo comprobarlo; obligaría a asumir.

## DRY-RUN

Lecturas previas: `lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, TaskDoc/resultado de la tarea Python, `test_treesitter_symbols.py`, `test_anchors.py`, `CHANGELOG.md`. Cambios previstos: readers nuevos en módulos nuevos de `sldb.code` que extraigan `calls`, `attrs.calls` y `attrs.handlers`; fixture frontend con componente que hace `fetch`, `axios` y botón `onClick`; tests; entrada de CHANGELOG. Dependencias: forma cerrada de la tarea Python; treesitter vía extra `code`; anclas TS. Validaciones futuras (sin ejecutar): los cinco comandos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`.

## FUTURO

Otro nodo/ejecutor aporta el esquema exacto de la tarea Python. Un humano decide el canal y destinatario del «aviso a IR», autoriza o no fixtures fuera de `files`, y ejecuta commit y cierre.

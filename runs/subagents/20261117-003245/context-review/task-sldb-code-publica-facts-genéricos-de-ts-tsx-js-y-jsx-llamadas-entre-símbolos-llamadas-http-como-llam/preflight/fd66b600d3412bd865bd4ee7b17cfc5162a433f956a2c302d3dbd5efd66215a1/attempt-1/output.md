## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1`, ampliar `sldb.code` para que los readers de TS, TSX, JS y JSX publiquen facts sintácticos genéricos, sin interpretar frameworks. Resultado: relación `calls` desde funciones, componentes y hooks hacia nombres llamados, con `attrs.calls = {func, line, first_arg}`; `attrs.handlers` en componentes con `{element, attribute, handler}` para atributos JSX `on*`; relación `calls` también hacia el handler. Incluye fixture, tests, CHANGELOG y commit. Límites: no interpreta REST/frameworks, no resuelve imports, no toca Python. Validación: los cinco comandos listados y `tools/check.sh --fast`.

## AMBIGUEDADES

1. «Mismas convenciones de forma que la tarea de Python (si esa ya cerró, seguir su forma exacta)»: no identifica la tarea ni su esquema; `depends_on: []`. Obligaría a inventar qué documento consultar y su forma exacta.
2. «Readers nuevos en módulos nuevos del paquete sldb.code»: `files` solo lista `lang_ts.py` y `ts_readers.py`. Obligaría a inventar nombres y ubicación de módulos.
3. «first_arg es el texto de un primer argumento literal (string o template sin expresiones) o null»: no dice si conserva comillas/backticks. Obligaría a inventar normalización.
4. «{element, attribute, handler}»: no define qué es `element` (tag, componente, expresión). Obligaría a inventar su valor.
5. «cuyo valor es un identificador o una llamada»: no aclara qué nombre registrar para `onClick={() => ...}` o `onClick={obj.fn}`. Obligaría a inventar la extracción.
6. «hacia cada nombre llamado (texto calificado tal cual)»: no fija granularidad para cadenas como `api.posts.create(...)` ni llamadas anidadas. Obligaría a inventar el criterio.
7. «las anclas TS existentes no cambian de estado»: no define baseline ni «estado». Obligaría a inventar el criterio de comparación.

## DRY-RUN

Lecturas: TaskDoc, `lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, tarea Python si existe, fixture y tests citados. Cambios previstos: readers nuevos, integración en el paquete, fixture TSX con `fetch`, `axios` y `onClick`, tests en `tests/selfdoc/test_treesitter_symbols.py`, CHANGELOG y commit. Dependencias: extras `code`/`dev`, tree-sitter y la forma cerrada de Python. Validaciones futuras: los cinco comandos de Validation, sin ejecutar ahora.

## FUTURO

Un humano o nodo previo debe identificar la tarea Python y aprobar el esquema; IR09 consumirá los facts; el revisor valida el resultado conjunto.

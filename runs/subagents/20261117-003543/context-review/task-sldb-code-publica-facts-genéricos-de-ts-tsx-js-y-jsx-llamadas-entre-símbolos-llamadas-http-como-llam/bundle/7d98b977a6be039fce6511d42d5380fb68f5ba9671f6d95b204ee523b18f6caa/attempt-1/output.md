## REFORMULACION

Encargo ejecutable de `sldb.code`: ampliar los facts de TS, TSX, JS y JSX (reader único ya existente) con (1) relación `calls` desde cada función, componente o hook hacia cada nombre llamado, con `attrs.calls` = `{func, line, first_arg}` y `first_arg` literal o `null`; (2) `attrs.handlers` en componentes, `{element, attribute, handler}` para atributos JSX `on*` con identificador o llamada, más `calls` hacia ese handler; (3) misma forma que la tarea de Python; fixture en `tests/fixtures/treesitter/frontend/src/`, tests, CHANGELOG y aviso a IR. Repo: `src/sldb/code/lang_ts.py`, `ts_readers.py`, `tests/selfdoc/test_treesitter_symbols.py`, `CHANGELOG.md`. Límites: no interpretar REST ni frameworks, no resolver imports, no Python.

## AMBIGUEDADES

1. «Mismas convenciones de forma que la tarea de Python (si esa ya cerró, seguir su forma exacta)»: no hay `depends_on` ni referencia a esa tarea; si no cerró, obligaría a inventar la forma de `calls`.
2. «first_arg es el texto de un primer argumento literal (string o template sin expresiones) o null»: no aclara si el texto conserva comillas; obligaría a inventar la normalización.
3. «relación calls … hacia cada nombre llamado (texto calificado tal cual)»: no aclara si una cadena como `api.posts.create` es un nombre o varios; obligaría a inventar la calificación.
4. «lista de {element, attribute, handler}»: no define qué es `element` (tag, nombre JSX, otro); obligaría a inventar su valor.
5. «Readers nuevos en módulos nuevos» frente a `files` que solo lista `lang_ts.py`/`ts_readers.py`: obligaría a inventar nombres de módulo.

## DRY-RUN

Lecturas: `lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, forma de `calls` de la tarea de Python (si existe), fixture frontend y tests actuales. Cambios previstos: readers nuevos de llamadas y handlers JSX; extensión de `_definition_fact` para `attrs.calls`/`attrs.handlers` y `relations`; fixture con fetch, axios y `onClick`; tests; CHANGELOG. Dependencias: gramática `tree-sitter-typescript`, `Ids`, forma de Python. Validaciones futuras: los cinco comandos de Validation, más aserciones de URLs literales, `calls` al handler, `onClick` en `attrs.handlers` y anclas TS sin cambio de estado.

## FUTURO

IR09/specIR interpreta los facts; un humano o nodo decide la forma de Python si esa tarea no cerró; `deskops closeout` gestiona commit, Board y aviso a IR.

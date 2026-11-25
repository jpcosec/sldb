## REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: que `sldb.code` publique facts genéricos de TS/TSX/JS/JSX con (1) relación `calls` desde cada función, componente o hook hacia el texto calificado llamado y `attrs.calls` con `{func, line, first_arg}`; (2) `attrs.handlers` en componentes para atributos JSX `on*` con valor identificador o llamada, más `calls` hacia ese handler. Resultado: readers nuevos en `sldb.code`, fixture en `tests/fixtures/treesitter/frontend/src/`, tests, CHANGELOG y aviso a IR. Límites: no interpretar REST/frameworks, no resolver imports, no Python. Depende de `task-sldb-code-publica-facts-genéricos-de-python...`.

## AMBIGUEDADES
1. «si esa ya cerró, seguir su forma exacta»: si la tarea Python no cerró, no hay forma exacta observable; obligaría a inventar el esquema de `calls`/`attrs.calls`.
2. «llamadas que hace cada función, componente o hook»: no aclara si incluye funciones anidadas/locales; obligaría a inventar el alcance del recorrido.
3. «cuyo valor es un identificador o una llamada»: no define qué `handler` se registra en una llamada JSX (`onClick={handleSave()}`) ni si se extrae el nombre interno; obligaría a inventar la semántica.
4. «fixture con un componente que hace fetch y axios y tiene un botón con onClick»: no fija archivos, nombres ni literales esperados; obligaría a inventar el fixture y las aserciones.

## DRY-RUN
Lecturas futuras: `src/sldb/code/lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, tests existentes, fixture frontend, resultado de la tarea Python y `CHANGELOG.md`. Cambios previstos: módulos nuevos de readers de llamadas/handlers; integrarlos en `scan_ts_file`; añadir `relations` tipo `calls` y `attrs.calls`/`attrs.handlers`; crear fixture y tests en `test_treesitter_symbols.py`; actualizar CHANGELOG. Dependencias: forma cerrada de Python, runtime tree-sitter TS/TSX, anclas existentes. Validaciones futuras: los cinco comandos listados, revisión de anclas y `tools/check.sh --fast`. No se ejecuta nada.

## FUTURO
Un humano debe resolver las ambigüedades o cerrar la tarea Python. Un ejecutor futuro implementará y ejecutará validaciones. IR/specIR interpretará los facts publicados. `deskops` cerrará, commiteará y actualizará el Board.

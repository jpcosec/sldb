## REFORMULACION
Nodo ejecutable `task.code` en `/mnt/ssd/proyectos/SLDB_1`: ampliar `sldb.code` para que TS, TSX, JS y JSX publiquen facts genéricos con llamadas entre símbolos, llamadas HTTP (`fetch`, `axios.*`, `api.*`) y handlers JSX, sin interpretar frameworks. Resultado: `attrs.calls` (`{func|name, line, first_arg}`), relación `calls`, `attrs.handlers` en componentes, fixture, tests y CHANGELOG. Límites: no resolver imports, REST ni Python; seguir la forma de la tarea Python; readers nuevos autorizados en módulos nuevos.

## AMBIGUEDADES
1. `"attrs.calls con {func, line, first_arg}"` frente a `"name en attrs.calls"`: obliga a inventar si la clave es `func` o `name`.
2. `"si esa ya cerró, seguir su forma exacta"`: si la tarea Python no cerró, obliga a inventar la forma canónica.
3. `"first_arg es el texto de un primer argumento literal"` frente a `"el valor del literal sin comillas ni backticks"`: obliga a decidir escapes y normalización interna.
4. `"cuyo valor es un identificador o una llamada"` frente al fixture que espera `onClick={() => { go(1); }}` como handler `go`: obliga a inventar la extracción desde arrows/IIFEs.
5. `"El diff de los intentos anteriores está en el árbol o en runs/subagents/..."`: obliga a elegir el punto de partida.
6. `"módulos nuevos ... autorizados aunque no figuren en files"` frente a `files` con `lang_ts.py`/`ts_readers.py`: obliga a decidir qué módulos crear.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, rituales, átomo, `lang_ts.py`, `ts_readers.py`, módulos de calls/JSX existentes, la tarea Python y el fixture. Crearía o ajustaría readers de llamadas y handlers, añadiría fixture TSX con `fetch`, `axios`, `api.*`, símbolos y eventos JSX, tests en `test_treesitter_symbols.py`, y CHANGELOG. Dependencias: tarea Python, extra `code` y gramática TS. Validaría después con los cinco comandos listados; no se ejecuta nada aquí.

## FUTURO
Otro nodo debe cerrar la tarea Python y fijar su forma exacta; un humano o IR debe aceptar la clave final, la extracción de handlers y el punto de partida; closeout decide commit, CHANGELOG y aviso a IR.

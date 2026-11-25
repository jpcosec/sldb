REFORMULACION
Propósito: ampliar `sldb.code` para publicar facts sintácticos genéricos de TS, TSX, JS y JSX, sin interpretar frameworks ni resolver imports. Resultado: relación `calls`, `attrs.calls` con `{func, line, first_arg}` y `attrs.handlers` con `{element, attribute, handler}`; fixture, tests y CHANGELOG; anclas TS sin cambios. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb.code` y `tests/selfdoc`. Límites: fuera REST, frameworks, imports, Python; depende de la tarea de facts de Python; se autorizan readers en módulos nuevos aunque no estén en `files`.

AMBIGUEDADES
1. “sigue su forma exacta para calls, attrs.calls y kwargs cuando aplique” y “si esa ya cerró”: obliga a inventar el esquema exacto y qué `kwargs` aplican si no se localiza el resultado cerrado de la tarea Python.
2. “Los readers nuevos van en módulos nuevos del paquete sldb.code”: no se nombran; obliga a inventar módulos y su ubicación.
3. “El diff de los intentos anteriores está en el árbol o en runs/subagents/20261116-exec-k4-c1/”: no fija cuál usar; obliga a inventar la base de partida.
4. “desde cada función, componente o hook” y “attrs.handlers en componentes”: no define cómo reconocer componentes/hooks; obliga a inventar heurísticas sintácticas.

DRY-RUN
Lecturas: TaskDoc, resultado de la tarea Python dependiente, inbox referenciado, `lang_ts.py`, `ts_readers.py`, `ts_fingerprints.py`, tests existentes y diff indicado. Cambios previstos: readers nuevos, integración en `sldb.code`, fixture en `tests/fixtures/treesitter/frontend/src/`, tests en `test_treesitter_symbols.py`, CHANGELOG y commit. Dependencias: forma canónica de Python, reader treesitter TS/JSX y estabilidad de anclas. Validaciones futuras: los cinco comandos listados, incluido `tools/check.sh --fast`.

FUTURO
La tarea Python dependiente aporta la forma canónica; IR consume los facts publicados; un humano resuelve las ambigüedades; los testers ejecutan las validaciones.

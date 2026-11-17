# Resultado — deskops-e-aa0321c9f2c0

Tarea: task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene. Pills: ninguno.

## Cambios
- `docs/user-manual.md` §10 "HTTP (`sldb serve`)": la lista de 6 rutas pasa a ser una tabla con una fila por ruta
  (`MÉTODO /path` | parámetros | qué devuelve), 57 rutas (40 GET, 17 POST), sacadas leyendo cada handler de
  `src/sldb/cli/serve/`. La única con tramo variable se escribe como en el código: `GET /views/<name>`.
  §16: "los 6 endpoints HTTP" pasa a "las rutas HTTP de la tabla de la seccion 10 (que un test compara con el codigo)".
- `tests/test_serve.py` (al final): `_dict_routes`, `_dispatcher_routes`, `_PATH_PARAM_ROUTES`, `_manual_routes`,
  `test_user_manual_lists_every_serve_route` (código ⇄ manual, las dos direcciones) y
  `test_documented_path_param_route_is_served` (`GET /views/no-such-view` es 404 de vista, no "Unknown route").
- `CHANGELOG.md`: entrada al inicio de 0.1.13.

## Done When
- Validation pasa con el test nuevo: los 3 comandos rc=0 (ver validation.log). 63 passed en test_serve.py,
  1206 en test_clean_code_rules.py, check.sh --fast "TODAS LAS PUERTAS PASAN".
- El test detecta la deriva: quitando la fila `GET /similar` del manual falla con
  "rutas de sldb serve que el manual no nombra: ['GET /similar']" (probado y revertido).
- CHANGELOG: hecho. Commit: no (prohibido al executor; lo hace el cierre).

## Comandos
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py` → rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` → rc 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` → rc 0
- Extra, informativo: `tools/check_claims.py` (no está en --fast): 11 afirmaciones falsas, todas preexistentes y
  ajenas (docs/architecture/selectors.md, views.md y entradas viejas del CHANGELOG: `docs/missing`, `docs/ambiguous`,
  `sldb query`); ninguna en docs/user-manual.md ni en la entrada nueva.

## Archivos tocados
- docs/user-manual.md
- tests/test_serve.py
- CHANGELOG.md
(+ runs/subagents/20261116-exec-srv/validation.log y result-summary.md)

## Desvío respecto de la Precisión
La precisión pide que la lista del código salga "de los dicts de rutas de routes.py y los *_routes.py importados en
el test". El código no cuadra del todo: solo una parte de las rutas vive en dicts/tuplas importables
(`EDGE_ROUTES`, `GRAPH_ROUTES`, `PROJECT_GRAPH_ROUTES`, `DOCUMENT_ROUTES`, `models_routes._GET_ROUTES/_POST_ROUTES`,
`notations_routes._NOTATION_ROUTES/_VIEW_ROUTES`, `docs_routes._ACTION_ROUTES`); otras 25 se despachan en `routes.py`
con cadenas `if route == "/x"` (y `route != "/save"`) y un dict local dentro de `dispatch_get`, sin nada importable.
Sin tocar `src/` (fuera del contrato; "no entra cambiar rutas"), el test importa los dicts que existen y lee esas
comparaciones de `routes.py` con `ast` (no regex): método POST si están en `dispatch_post`, GET si no. `GET /views/<name>`
(nombre por `removeprefix` en `views_routes`) va como constante explícita en el test y otro test comprueba que el
servidor la sirve. Si se prefiere la forma pura, la continuación sería mover esos despachos de `routes.py` a un dict
importable (tarea aparte, toca src).

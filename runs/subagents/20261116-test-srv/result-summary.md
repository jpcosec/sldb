# Tester deskops-t-547cfa20586c — task-la-documentación-de-sldb-serve-nombra-todas-sus-rutas-http-con-un-chequeo-que-lo-mantiene

**Veredicto: PASA**

Evidencia completa en `validation.log` (Validation + mutaciones + sonda en vivo). Scripts propios fuera del repo:
`/dev/shm/t547-scripts/mutate.sh` y `/dev/shm/t547-scripts/probe.py`.

## Validation (corrida propia)
| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py` | PASA: 63 passed, rc 0 |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` | PASA: 1206 passed, rc 0 |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` | PASA: "TODAS LAS PUERTAS PASAN", rc 0 |

`uv` funcionó; no hizo falta el fallback. Validation no nombra la suite completa ni `sldb stores build --check`.

## Done When
- **El documento lista cada ruta (método, path, parámetros, retorno):** PASA. `docs/user-manual.md` §10 tiene ahora una tabla de 57 filas
  (40 GET, 17 POST) con la primera columna `MÉTODO /path`. La sonda en vivo (`probe.py`) levanta `sldb serve` sobre un store de
  prueba y pide las 57 filas con su método: ninguna responde "Unknown route" ni 405 (`GET /views/<name>` → 404 de vista, que es lo
  esperado). Controles negativos (`GET /nope`, `POST /nope`, `GET /save`, `POST /similar`, `GET /views/a/b`,
  `POST /models/detail`, `GET /graph/nope`) → 404 "Unknown route". La afirmación de §16 sobre "los 6 endpoints HTTP" cita ahora la tabla de §10.
- **El test falla si una ruta del código falta en el documento o viceversa:** PASA (ver Robustez).
- **Los comandos de Validation pasan con el test nuevo:** PASA (arriba).
- **CHANGELOG:** PASA. Hay una entrada al inicio de 0.1.13 y lo que afirma coincide con el diff (57 = 40+17, los nombres de los tests, la lectura con ast).
- **Commit:** no aplica al tester; queda para el cierre.

## Robustez del desvío aceptado (lectura con ast) — pedido del coordinador
Cada mutación se hizo en una copia fresca en `/dev/shm/srvcopy-t547`, ya borrada, y corre solo `test_user_manual_lists_every_serve_route`:
| # | Mutación | Resultado |
|---|---|---|
| M0 | sin cambios (control) | passed |
| M1 | `if route == "/nuevo-get"` en `routes._dispatch_reader` | FALLA: `['GET /nuevo-get']` ✔ |
| M2 | `if route == "/nuevo-post"` en `routes.dispatch_post` | FALLA: `['POST /nuevo-post']` ✔ |
| M3 | `"/models/nueva"` en `models_routes._GET_ROUTES` | FALLA: `['GET /models/nueva']` ✔ |
| M4 | `"/docs/nueva"` en `docs_routes._ACTION_ROUTES` | FALLA: `['POST /docs/nueva']` ✔ |
| M5 | quitar la fila `POST /save` del manual | FALLA: `['POST /save']` ✔ |
| M6 | quitar la fila `GET /views/<name>` del manual | FALLA: `['GET /views/<name>']` ✔ |
| M7 | cambiar el método en el manual (`POST /similar`) | FALLA, nombra la ruta ✔ |
| M8 | errata en el path del manual (`/similars`) | FALLA, nombra la ruta ✔ |
| M9 | fila sin backticks en el manual | FALLA (la fila se ignora y falta la ruta) ✔ |
| M10 | fila duplicada en el manual | passed (el test no lo detecta) |
| M11 | **borde:** un `foo_routes.py` nuevo con su propio dict `FOO_ROUTES`, despachado desde `routes.py` con `route.startswith("/foo/")` | **passed: el test NO detecta `GET /foo/a`** |

Los casos que pidió el coordinador (ruta nueva en `routes.py` y en un `*_routes.py` existente, fila quitada del manual) fallan y
nombran la ruta. Límite que queda, que no bloquea: el test enumera a mano los módulos con dict (`_dict_routes`). Un módulo nuevo
de rutas, o una rama nueva que se despacha por prefijo (`startswith`), pasa sin aviso (M11). Lo mismo vale para un
`if route == "/views/x"` agregado dentro de `views_routes.py`, porque ast solo recorre `routes.py`. La forma pura que propone el
ejecutor (un registro único e importable de rutas en `src/`) lo cerraría; sería una tarea aparte, porque toca `src/`. M10
(filas duplicadas) es cosmético.

## 5 filas al azar contra su handler (`random.seed(547)`)
| Fila | Handler | ¿Coincide? |
|---|---|---|
| `GET /docs/select` | `docs_select_routes.dispatch_docs_select`: params ref, prefix, path_glob, model, where, include_linked, one; 404 si no hay ninguno y 409 con `candidates` si hay varios, con `one` | Sí |
| `GET /document/ir` | `document_routes`: `id` requerido (400), 404 si no está trackeado, devuelve el IR solo (`_respond_ir`), 422 si no se construye | Sí |
| `POST /extract/segments` | `segments_routes.extract_segments_response`: body `{model, markdown}`, 404 por el modelo y 422 por el contenido | Sí |
| `GET /graph/isolated` | `graph_routes.isolated_payload`: sin params, `{isolated}` | Sí |
| `GET /health` | `health.health_payload`: `{status: ok\|degraded, findings, action}` | Sí |

## Alcance y regresiones
- Archivos tocados por el ejecutor: `docs/user-manual.md`, `tests/test_serve.py` y `CHANGELOG.md`, los tres del contrato. Ningún cambio en `src/`.
  Los demás cambios del árbol (`.sldb/`, `desk/tasks/`, `desk/reviews/`, `runs/`) son del coordinador o ajenos y no los revisé.
- Regresiones vecinas: `git diff --name-only` no muestra módulos de `src/` cambiados, así que no hay importadores que correr.
  `tests/test_serve.py` pasa entero (63).
- Clean code: `test_clean_code_rules.py` y `check.sh --fast` pasan con los archivos tocados.

## Observación (fuera de alcance, preexistente)
En la sonda, `POST /save` y `POST /docs/track` con body `{}` responden **500** en vez de 400. La tarea no cambia rutas y el manual no
promete otro status para ese caso. Se anota como posible tarea aparte.

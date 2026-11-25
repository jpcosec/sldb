## REFORMULACION

Propósito: que la documentación de `sldb serve` nombre **todas** sus rutas HTTP (hoy 5 de ~45) y que un test lo mantenga sincronizado con el código. Resultado: un documento con una entrada por ruta (método, path, parámetros, retorno en una línea) + un test en `tests/test_serve.py` que falla ante cualquier ruta del código ausente del documento **o** documentada sin existir en el código + entrada de CHANGELOG. Repo: SLDB_1. Límites: no se cambian rutas; superficie tocada `docs/` (documento de serve), `tests/test_serve.py`, `CHANGELOG.md`. Nodo ejecutable (task.code) en `ritual-execution`.

## AMBIGUEDADES

1. "encontrar el documento actual de serve (docs/user-manual.md u otro de docs/ que lo describa)" — no fija el archivo destino; obligaría a inventar si se amplía §10 del manual o se crea un documento nuevo.
2. "5 de unas 45 rutas que define src/sldb/cli/serve/" — el número es aproximado y no se dice qué cuenta como ruta (¿solo las registradas en `http_server.py`, o también helpers de los `*_routes.py`?); inventar el criterio de enumeración.
3. "método, path, parámetros y qué devuelve en una línea" — no define formato (tabla, ficha por ruta) ni cómo se marca una ruta para que el test la lea; inventar convención de parseo.
4. "un test falla si una ruta del código no está en el documento o viceversa" — no dice de dónde sale la lista canónica del código ni cómo se extrae la del Markdown; inventar el mecanismo de comparación.
5. El manual afirma en §16 "los 6 endpoints HTTP … Verificado en vivo y sin cambios"; completar §10 contradice esa afirmación y el input no dice si debe reescribirse; obligaría a inventar el alcance de la corrección.

## DRY-RUN

Lecturas: `src/sldb/cli/serve/http_server.py` y cada `*_routes.py` (registro real), `docs/user-manual.md` (§10, §16), `tests/test_serve.py`, `tools/check.sh`, `CHANGELOG.md`. Cambios previstos: ampliar el documento con todas las rutas; añadir test que enumere rutas registradas y las compare contra las documentadas (fallo bidireccional); entrada CHANGELOG. Dependencias: un punto de enumeración estable de rutas en el código; una convención de marcado en el documento parseable por el test. Validaciones futuras: los tres comandos de la sección Validation del TaskDoc, más `tools/check.sh --fast`.

## FUTURO

Un ejecutor futuro implementa y valida; el humano decide el archivo destino y la convención de marcado (ambigüedades 1–5) antes de ejecutar. El cierre (commit, CHANGELOG, retiro del Board) lo resuelve `deskops closeout`; la auditoría de contexto y de historial git corresponde al ritual de execution/closeout.

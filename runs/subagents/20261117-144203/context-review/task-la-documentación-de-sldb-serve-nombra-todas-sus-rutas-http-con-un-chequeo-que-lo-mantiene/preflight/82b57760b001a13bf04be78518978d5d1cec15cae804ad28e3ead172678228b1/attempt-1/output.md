REFORMULACION
El encargo es completar la documentación de `sldb serve` para que enumere todas las rutas HTTP registradas en `src/sldb/cli/serve/` —método, path, parámetros y retorno en una línea— y añadir en `tests/test_serve.py` un test que falle si una ruta del código falta en el documento o viceversa. Repo: `SLDB_1`. Resultado: documento actualizado, test, entrada en `CHANGELOG.md` y commit. Límites: no cambiar rutas; validar con pytest y `tools/check.sh --fast`.

AMBIGUEDADES
1. «docs/user-manual.md u otro de docs/ que lo describa»: no fija el documento canónico; obligaría a inventar cuál usar.
2. «método, path, parámetros y qué devuelve en una línea»: no define formato ni nivel de detalle de parámetros (path/query/body) y respuesta; obligaría a inventar la representación.
3. «un test ... que compare las rutas registradas con las del documento»: no indica cómo extraer rutas del documento ni del código; obligaría a inventar parser o estrategia de comparación.
4. «todas las rutas registradas»: no aclara si cuentan aliases, múltiples métodos, rutas dinámicas o generadas; obligaría a inventar el criterio.
5. «CHANGELOG y commit»: no fija formato de entrada ni convención de commit; obligaría a inventar ambos.

DRY-RUN
Lecturas: `docs/user-manual.md` y resto de `docs/`; `tests/test_serve.py`; `src/sldb/cli/serve/http_server.py` y `*_routes.py`; `CHANGELOG.md`. Cambios previstos: elegir el documento de serve, añadir la tabla completa de rutas, crear o ampliar el test comparador y registrar el cambio en CHANGELOG. Dependencias: API de registro de rutas, utilidades de test y criterio de parseo documental. Validaciones futuras: los tres comandos de `Validation`. Sin ejecutar nada.

FUTURO
Un nodo ejecutor materializará documento, test y CHANGELOG; otro nodo o un humano ejecutará las validaciones y el commit, y decidirá si el documento elegido y el nivel de detalle son aceptables.

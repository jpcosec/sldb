REFORMULACION
Nodo ejecutable (`task.code`). Propósito: que la documentación de `sldb serve` enumere todas sus rutas HTTP y quede protegida por un test. Resultado: en `docs/user-manual.md` §10, una tabla con una fila por ruta y primera columna `MÉTODO /path`, con parámetros y retorno en una línea; §16 cita esa tabla; `tests/test_serve.py` compara las rutas de los dicts de `src/sldb/cli/serve/` con las de la tabla; CHANGELOG. Repo: SLDB_1 (`sldb`). Límites: no cambiar rutas; la lista del código se importa, no se extrae por regex; el TaskDoc no liga pills ni átomos.

AMBIGUEDADES
1. “método, path, parámetros y qué devuelve en una línea” frente a “primera columna `MÉTODO /path`”: no define columnas para parámetros/retorno ni su formato. Obligaría a inventar columnas y nivel de detalle.
2. “La lista del código sale de los dicts de rutas … importados en el test”: no describe las claves ni la estructura de esos dicts. Obligaría a inventar el mapeo a método, path, parámetros y retorno.
3. “la del documento sale de la primera columna de esa tabla”: no fija cómo separar método y path, ni normalizar parámetros o espacios. Obligaría a inventar el parser.
4. “qué devuelve en una línea”: no aclara si es esquema, ejemplo JSON o códigos de error. Obligaría a inventar el resumen.
5. “CHANGELOG”: no especifica entrada ni redacción. Obligaría a inventar el texto.

DRY-RUN
Lecturas: §10 y §16 de `docs/user-manual.md`; `src/sldb/cli/serve/http_server.py`, `routes.py` y `*_routes.py`; `tests/test_serve.py`; CHANGELOG; rituales execution/testing/closeout. Cambios previstos: reemplazar la lista HTTP de §10 por la tabla completa; corregir §16; añadir test que importe los dicts, lea la primera columna y compare conjuntos; entrada CHANGELOG. Dependencias: dicts importables y estables, tabla parseable, entorno `uv`. Validaciones futuras: los tres comandos indicados. No se ejecutó nada.

FUTURO
Otro nodo debe inspeccionar los dicts y fijar el contrato de tabla/parser; un humano decide la redacción del CHANGELOG y confirma la cita de §16. La ejecución futura produce tabla, test y CHANGELOG, y corre las validaciones.

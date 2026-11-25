## REFORMULACION
Encargo ejecutable en `/mnt/ssd/proyectos/SLDB_1/sldb`: en el manejador de `POST /save` de sldb serve, cuando pydantic rechace un documento, responder 422 con `details` igual a `exc.errors()` serializable (`loc`, `msg`, `type`), conservando lo ya devuelto. Resultado: cambio en `src/sldb/cli/serve/` y test nuevo `tests/test_serve_save_422.py` que use un modelo con campo `int`, envíe `"abc"`, espere 422 y verifique `body['details']` como lista no vacía con `loc` que nombre el campo. Límites: solo ruta save y un test; fuera el resto de serve. No es agregado ni paquete.

## AMBIGUEDADES
1. “`exactamente la lista exc.errors() (serializable: loc, msg, type)`”: no queda claro si se devuelve `exc.errors()` completo o solo esos tres campos. Obliga a inventar una proyección/filtrado o asumir que no habrá claves extra.
2. “`un modelo minimo con un campo int, save con ese campo en 'abc'`”: falta la forma exacta del payload, registro del modelo y ruta/app de prueba. Obliga a inventar el cuerpo de la petición y el montaje del test.
3. “`siguiendo cualquier test existente de serve (grep -ln 'serve' tests/)`”: no se nombra archivo ni fixture/cliente. Obliga a elegir un patrón de test no especificado.
4. “`ademas de lo que ya devuelve`”: no se describe el 422 actual. Obliga a inferir su forma o inventar compatibilidad si no se inspecciona el código.
5. “`loc que nombra el campo`”: no define cómo comprobar que “nombra”. Obliga a inventar una aserción concreta.

## DRY-RUN
Lecturas previstas: buscar el handler en `src/sldb/cli/serve/`, localizar la captura de `ValidationError`, revisar tests de serve y la serialización existente. Cambios previstos: añadir `details` en el 422 y crear `tests/test_serve_save_422.py`. Dependencias: pydantic/FastAPI, cliente de test y fixtures existentes. Validación futura: ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_serve_save_422.py`. Nada se ejecuta aquí.

## FUTURO
El nodo ejecutor inspeccionará el código real y producirá el diff y la salida de pytest; un humano o nodo revisor decidirá si la serialización debe ser literal o filtrada y si el 422 mantiene compatibilidad.

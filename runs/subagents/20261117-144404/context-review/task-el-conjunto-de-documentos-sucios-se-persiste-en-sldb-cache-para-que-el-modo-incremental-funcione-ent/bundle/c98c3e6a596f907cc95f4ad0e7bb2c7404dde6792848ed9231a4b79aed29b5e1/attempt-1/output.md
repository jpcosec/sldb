REFORMULACION
Propósito: que el conjunto de documentos sucios de `documents_dirty.py` sobreviva entre procesos para habilitar el modo incremental V2. Resultado: persistirlo y leerlo en `.sldb_cache` con escritura atómica bajo el lock del store, invalidarlo cuando cambie la firma del store y caer al cálculo completo sin error si falta o está corrupto; añadir tests con subprocess y CHANGELOG. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1`), con `src/sldb/store/documents_dirty.py`, `tests/store/test_merkle_operation_cache.py` o un test de store existente, y `CHANGELOG.md`. Límites: no versionar el archivo de caché ni cambiar qué se considera sucio.

AMBIGUEDADES
1. “El conjunto de documentos sucios se guarda en .sldb_cache” / “persistir y leer el conjunto en .sldb_cache”: no fija ruta, nombre, formato ni esquema; obliga a inventar serialización y ubicación.
2. “invalidarlo cuando cambia la firma del store”: no define qué es la “firma” ni cómo detectar el cambio; obliga a inventar su cálculo y almacenamiento.
3. “bajo el lock del store”: no identifica API, ruta ni alcance del lock; obliga a inventar el mecanismo de bloqueo.
4. “una corrida nueva lo lee”: no dice cuándo (inicio, primer acceso) ni cómo convive con el diccionario en memoria; obliga a inventar el ciclo de carga.
5. “se vuelve al cálculo completo sin error”: no define “cálculo completo” por namespace ni si el archivo corrupto se borra o reescribe; obliga a inventar el fallback.

DRY-RUN
Lecturas: `documents_dirty.py`, `documents_hash.py`, `user_cache.py`, consumidores del dirty set, helpers de lock/rutas de store, tests existentes y CHANGELOG. Cambios previstos: persistencia y carga en `documents_dirty.py`, escritura atómica bajo lock, invalidación por firma y fallback; tests nuevos con subprocess; entrada de CHANGELOG. Dependencias: helper de caché, API de lock, definición de firma, pytest/uv. Validaciones futuras: los cinco comandos listados, primero el test específico y luego `tools/check.sh --fast`.

FUTURO
Un humano o nodo de contexto debe fijar formato, lock y firma si no se resuelven antes. El ejecutor implementará el cambio; el ritual de testing correrá las validaciones; closeout actualizará CHANGELOG, hará commit atómico y deskops retirará la tarea del Board.

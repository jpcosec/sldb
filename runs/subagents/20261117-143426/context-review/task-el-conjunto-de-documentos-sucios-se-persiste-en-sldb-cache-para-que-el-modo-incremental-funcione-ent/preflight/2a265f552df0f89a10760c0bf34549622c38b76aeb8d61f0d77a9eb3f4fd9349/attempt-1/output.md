## REFORMULACION

**Propósito:** hacer que el conjunto de documentos sucios de `src/sldb/store/documents_dirty.py` sobreviva entre procesos mediante `.sldb_cache`, para que el modo incremental V2 solo procese cambios reales.

**Resultado:** persistencia y lectura del conjunto con escritura atómica bajo el lock del store; invalidación al cambiar la firma del store; fallback silencioso al cálculo completo si falta o está corrupto; tests y CHANGELOG.

**Repo:** `/mnt/ssd/proyectos/SLDB_1`.

**Límites:** no versionar el archivo ni cambiar qué se considera sucio. El nodo es una tarea ejecutable (`task.code`), no un agregado.

## AMBIGUEDADES

1. “se guarda en .sldb_cache”: no se define ruta exacta, nombre de archivo ni formato de serialización; obligaría a inventarlos.
2. “invalidarlo cuando cambia la firma del store”: no se especifica qué constituye la firma ni cómo detectar su cambio; obligaría a inventar el mecanismo.
3. “bajo el lock del store”: no se identifica la API concreta del lock ni su alcance; obligaría a elegir una implementación.
4. “tests en tests/store/test_merkle_operation_cache.py o un archivo de tests de store existente”: permite más de una ubicación sin criterio de elección; obligaría a decidir.
5. “si el archivo falta o está corrupto, se vuelve al cálculo completo sin error”: no define qué cuenta como corrupción ni si debe registrarse algo; obligaría a inventar validación y logging.

## DRY-RUN

**Lecturas previstas:** `documents_dirty.py`, `user_cache.py`, consumidores del conjunto, utilidades de lock/rutas de `.sldb_cache`, tests de store y `CHANGELOG.md`.

**Cambios previstos:** serialización y escritura atómica del conjunto, lectura al inicio, validación de firma/corrupción, fallback al cálculo completo, tests con subprocess para proceso nuevo y archivo corrupto, entrada en CHANGELOG.

**Dependencias:** API de lock del store, ubicación/gestión de caché, formato del conjunto sucio, definición de firma.

**Validaciones futuras:** los cinco comandos de Validation y `bash tools/check.sh --fast`, con tests nuevos pasando.

## FUTURO

Quedan fuera de este nodo: la decisión humana de aceptar el resultado, la revisión del CHANGELOG y la creación del commit.

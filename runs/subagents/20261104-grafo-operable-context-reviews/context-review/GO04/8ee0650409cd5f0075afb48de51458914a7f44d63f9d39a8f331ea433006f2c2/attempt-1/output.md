REFORMULACION

GO04 es un nodo `code` de sldb, delivery bajo PK02. Encargo: que cada nodo del índice de aristas exponga una facet `payload` (campos escalares o listas de escalares, filtrada por `__indexed__` si existe) y que el shard guarde `source_hash` y `contract_signature`, con `EDGE_INDEX_VERSION` 5 y staleness por ambos; además, filtros de `StructuredQuery` sobre la facet sin re-extraer Markdown. Resultado: proyección consultable y detección correcta de ediciones externas. Repo dueño: sldb. Límites: no cambia resultados de consultas existentes, no implementa el lenguaje de GO05 ni estados de ancla de GO07.

AMBIGUEDADES

1. «un nombre cuyo valor no es proyectable es error al cargar el modelo»: no aclara si el error ocurre al cargar la definición del modelo, al cargar un documento o al construir el shard; obliga a inventar el momento y el sujeto de la validación.
2. «containment: ídem, compositions: ídem»: el «ídem» no nombra los atributos de clase que aportan `containment` y `compositions` (solo se nombra `__references__`); obliga a inventar de dónde se leen esos nombres y qué pasa si el modelo no los declara.
3. «editar el Markdown por fuera marca stale»: no dice en qué operación se detecta (abrir, consultar, reconstruir); obliga a inventar el disparador de la comprobación.

DRY-RUN

Un ejecutor futuro leería los módulos de `edge_index`, `edge_sync`, `compose`, `structural_queries` y `executor`, los modelos con `__indexed__`, la doc de backend y CHANGELOG. Cambiaría: construir `payload` y las cuatro claves, subir versión, calcular staleness por `source_hash` y firma, y añadir filtros de facet con error por campo no proyectado. Depende de GO03 (`GraphBackend` y proyección en `load`) y del gate `G_SEAM`; no depende de GO05/GO07. Validaría: cero `Validator.extract` en la consulta, stale por edición externa y por `__references__`, migración de shard v4, tests existentes de `StructuredQuery`, y medición de MB/shards antes y después.

FUTURO

GO05 consume la facet para el lenguaje; GO07 agrega `<campo>__anchor_state`; GO08 cablea `stores check`; deskops consume en su propio plan. El TaskDoc fijará nombres exactos de archivos, funciones y tests; el revisor y el dueño aceptan y validan mediciones. `G_SEAM` lo produce GO03, no GO04.

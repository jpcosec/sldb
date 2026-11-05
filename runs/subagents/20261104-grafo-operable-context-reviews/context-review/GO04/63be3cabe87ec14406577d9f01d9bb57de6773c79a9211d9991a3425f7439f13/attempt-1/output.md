## REFORMULACION
GO04 es un nodo `code`/`delivery`, no agregado, del repo `sldb`. Encarga proyectar al nodo del índice una facet `payload` plana con campos escalares o listas de escalares, omitiendo diccionarios y listas no escalares; agregar `payload`, `field_hashes`, `source_hash` y `contract_signature` al shard; subir `EDGE_INDEX_VERSION` de 4 a 5; marcar stale por versión, `source_hash` o `contract_signature` y reconstruir con el dirty set; y extender `StructuredQuery` y su executor para filtrar sobre la facet sin re-extraer Markdown. Resultado: shards v5 con proyección y staleness correcta, consultas estructuradas sobre campos proyectados, documentación de omisiones, CHANGELOG y métricas antes/después. Límites: no cambia resultados existentes, no re-extrae, no toca el `eval` de GO03; `output_scope` acotado a `edge_index/`, `edge_sync.py`, `facet_match.py`, `executor.py`, `structural_queries.py`, `graph-backend.md` y CHANGELOG. Depende de GO03; `G_SEAM` pending no es defecto.

## AMBIGUEDADES
1. “sobre una lista, contains es pertenencia y eq/ne comparan la lista entera, gt/lt dan false”: no define `starts_with` ni `is_null`/`is_not_null` sobre listas; obliga a inventar su resultado.
2. “Un filtro sobre un campo no proyectado (anidado, fuera de __indexed__ o inexistente en el modelo) es un error de consulta”: no cubre un campo de nivel superior omitido por ser diccionario o lista no escalar; obliga a decidir entre error y conjunto vacío.
3. “la reconstrucción ocurre en la siguiente reconstrucción del índice (la próxima escritura o stores build), con el dirty set existente”: no define cómo entran al dirty set los shards v4 marcados stale al abrir; la aceptación exige reconstruirlos en la siguiente escritura.
4. “field_hashes se agrega”: no dice si es el mapa completo del documento o solo el de campos proyectados; obliga a inventar el contenido del shard.

## DRY-RUN
Lecturas: GO04, `brief.md`, `alcance.md`, `decisiones.md`, `doc_structure.py`, `compose.py`, `edge_sync.py`, `facet_match.py`, `executor.py`, `structural_queries.py`, tests y CHANGELOG. Cambios previstos: constructor de proyección; cuatro claves de shard y versión 5; firma canónica; detección stale; filtros sobre payload. Dependencias: GO03/G_SEAM y dirty set existente. Validaciones futuras: proyección y omisión de anidados; edición externa y cambio de `__references__` marcan stale; cero llamadas a `Validator.extract`; shard v4 stale se reconstruye; tests existentes de `StructuredQuery`; métricas de tamaño y shards. Sin ejecutar.

## FUTURO
GO03 entrega la costura y `G_SEAM`; GO05 consume la facet. El operador del desk acepta la revisión y promueve el TaskDoc; allí se fijan nombres y tests exactos. El dueño indica el host de pytest.

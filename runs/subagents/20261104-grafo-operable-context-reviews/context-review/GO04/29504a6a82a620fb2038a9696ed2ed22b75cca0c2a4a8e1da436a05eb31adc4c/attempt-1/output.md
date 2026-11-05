## REFORMULACION

**Propósito:** GO04 (nodo `code`, `delivery`, repo `sldb`, padre PK02) proyecta al índice de aristas una facet `payload` con los campos escalares del payload, más `content_hash` y `field_hashes`; corrige `EdgeIndex.stale`; y habilita filtros de `StructuredQuery` sobre esa facet sin re-extraer Markdown.

**Resultado:** nodos con `payload`, `EDGE_INDEX_VERSION = 5`, reconstrucción de shards viejos, staleness por `source_hash` y firma de contrato del modelo, consultas por campo con cero llamadas a `Validator.extract`, y mediciones de tamaño/shards registradas.

**Repo dueño:** `sldb`. **Límites:** solo `output_scope` (`edge_index/`, `edge_sync.py`, `graph/facet_match.py`, `graph/executor.py`, `structural_queries.py`, `CHANGELOG.md`); depende de GO03 y requiere `G_SEAM`; ninguna ejecución está autorizada.

## AMBIGUEDADES

1. «sha256 de los nombres de campo declarados más `__references__`, `__containment__` y `__compositions__`»: no fija orden, separador, codificación ni si entran contenidos o solo nombres. El ejecutor tendría que inventar el formato canónico de la firma.
2. «los shards viejos se reconstruyen»: no dice el disparador (carga, escritura, detección de versión) ni si usa el dirty set. El ejecutor tendría que inventar cuándo y cómo migrar.
3. «StructuredQuery acepta filtros sobre la facet payload con sus operadores actuales (en structural_queries y el executor, dentro del output_scope)»: «el executor» no se identifica; el scope nombra `graph/executor.py` (eval de GO03), no un ejecutor de consultas. El ejecutor tendría que inventar el punto de integración.
4. «por defecto todos esos campos, o solo los nombres listados en el atributo de clase `__indexed__` si el modelo lo declara»: no aclara si `__indexed__` sustituye el conjunto por defecto ni qué pasa con un nombre listado ausente o anidado. El ejecutor tendría que inventar la regla.

## DRY-RUN

**Lecturas:** `dag.yaml`, brief/alcance/decisiones, contrato de GO03 y `G_SEAM`, modelos, `edge_index/`, `edge_sync.py`, `structural_queries.py`.

**Cambios previstos:** facet `payload` por nodo, clave `payload` en shard, versión 5, lógica de `stale`, filtros en `StructuredQuery`, tests y CHANGELOG.

**Dependencias:** GO03 (backend/costura), reglas comunes de ejecución.

**Validaciones futuras:** escritura proyecta escalares y omite anidados; edición externa del Markdown marca stale y reconstruye; cambio en `__references__` marca stale; consulta `status = closed` con cero `Validator.extract`; versión 5; MB y shards antes/después en Validation y CHANGELOG. Sin ejecutar.

## FUTURO

GO05 consume la facet para el lenguaje; GO07 consume `field_hashes` y anclas; la revisión de GO03 produce `G_SEAM`; el dueño indica host de pytest y acepta mediciones y promoción.

REFORMULACION
Propósito: que el índice de aristas de sldb lleve el payload de cada documento proyectado como facet escalar consultable, sin re-extraer Markdown, y que la detección de staleness del índice sea correcta. Resultado: cada nodo de documento gana `payload`, `field_hashes`, `source_hash` y `contract_signature`; `EDGE_INDEX_VERSION` pasa a 5; un shard de versión menor o con `source_hash`/firma de contrato distintos queda stale y se reconstruye en la siguiente reconstrucción con el dirty set existente; `StructuredQuery` filtra sobre la facet en `structural_queries.py` y su executor, con error nombrado para campos no proyectados y sin cambiar resultados existentes. Repo dueño: sldb. Límites: el `output_scope` listado; nada fuera de él; no re-extrae Markdown; depende de GO03 (G_SEAM).

AMBIGUEDADES
1. "un nombre cuyo tipo declarado en el modelo no es proyectable es error al registrar o cargar la definición del modelo": el input no dice dónde se declaran tipos de campo ni cómo se comprueba la proyectabilidad declarada; obligaría a inventar el mecanismo de tipos.
2. "fields: todos los nombres de campo declarados por el modelo, ordenados (no solo los proyectados)" (contract_signature): no aclara si incluye campos heredados vía `base_models` o solo los propios; obligaría a inventar el alcance de la firma, con efecto en cuándo un shard queda stale.
3. "StructuredQuery acepta filtros sobre la facet payload con sus operadores actuales": no define semántica de `gt`, `lt`, `contains`, `ne` sobre campos lista o null; obligaría a inventar comparación y pertenencia.
4. "Un filtro sobre un campo no proyectado (anidado o fuera de `__indexed__`) es un error de consulta": no cubre un campo inexistente en el modelo ni un campo escalar ausente en todos los payloads; obligaría a inventar si es error o conjunto vacío.

DRY-RUN
Lecturas: `edge_index/` (doc_structure, compose, edge_rebuild), `edge_sync.py`, `structural_queries.py`, `graph/executor.py`, definiciones de modelos y tests existentes. Cambios previstos: cuatro claves en el registro del nodo; versión 5; chequeo de staleness donde hoy se consulta, al abrir y antes de consulta/reconstrucción; `facet_match.py` con operadores; integración en `StructuredQuery`; doc de arquitectura y CHANGELOG. Dependencias: GO03/G_SEAM aporta el executor/backend; sin GO02. Validaciones futuras: tests de StructuredQuery sin cambios; stale por edición externa y por cambio de `__references__`; cero llamadas a `Validator.extract`; shard v4 stale; MB y shards antes/después.

FUTURO
GO05 usa la facet y la proyección para el lenguaje; GO07 usa `field_hashes` y la proyección para `anchor_state`. Un humano/deskops promueve el TaskDoc, fija nombres exactos y valida las mediciones.

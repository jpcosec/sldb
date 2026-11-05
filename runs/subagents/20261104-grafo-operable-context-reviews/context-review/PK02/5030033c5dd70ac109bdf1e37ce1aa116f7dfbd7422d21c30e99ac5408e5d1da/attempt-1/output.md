REFORMULACION
PK02 es un agregado de planificación (no ejecutable) cuyo propósito es dotar a sldb del sustrato para evaluar reglas: proyectar el payload a los nodos del grafo, corregir staleness y disponer de un único lenguaje de predicados que lea esos campos y cruce relaciones. Resultado: GO04 produce la facet payload, `field_hashes`, `source_hash` y `contract_signature`, versión 5 y detección de stale; GO05 implementa el lenguaje de GO02 sobre esa proyección y deja `where_parse` y `FieldCondition` como shims deprecados que avisan, sin retirarlos (GO10/PK04). Repo dueño: sldb. Límites: no se ejecuta como nodo; termina con GO04 y GO05; no cambia resultados de consultas existentes; no retira shims; no re-extrae Markdown.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético, sin ejecutar. Orden: GO04 → GO05 (GO05 depende de GO04). GO04: lee la costura de GO03/G_SEAM, `edge_index`, modelos y tests de `StructuredQuery`; cambia `edge_index` (payload, `field_hashes`, `source_hash`, `contract_signature`, `EDGE_INDEX_VERSION` 5), staleness, `facet_match`, executor, `structural_queries`, docs y CHANGELOG; salida: nodos con facet proyectada, stale por `source_hash` o firma de contrato, consultas estructuradas sin `Validator.extract`, mediciones de MB/shards. GO05: recibe G_SEMANTICS de GO02 y la proyección de GO04; captura primero goldens de `where_parse`/`FieldCondition` tal como quedan tras GO04; implementa parser/evaluador, enruta `where_matches`, `edges_holding`, `StructuredQuery` y `--where`; salida: lenguaje único, `any()`/`all()` con explicación, shims con `DeprecationWarning` y warnings del envelope, tests de equivalencia y xfail verdes. Validación conjunta: PK02 se acepta si el `--where` nuevo no re-extrae, `any()`/`all()` responde por CLI con explicación, los shims avisan (probado), equivalencia contra goldens pasa y GO04 no altera consultas existentes. Dependencias: GO04←GO03/G_SEAM; GO05←GO02/G_SEMANTICS y GO04.

FUTURO
GO10/PK04 decide y ejecuta el retiro de shims; el operador del desk de sldb acepta la revisión en frío y promueve hijos; el dueño valida pytest en el host indicado; deskops consume el resultado en su propio plan (G_CONSUMER).

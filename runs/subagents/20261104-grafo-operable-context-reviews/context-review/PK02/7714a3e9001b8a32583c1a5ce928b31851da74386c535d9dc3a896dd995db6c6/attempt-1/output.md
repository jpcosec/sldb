## REFORMULACION  
PK02 es un agregado de planificación del repo `sldb` cuyo propósito es dejar el sustrato del grafo listo: nodos con campos del payload proyectados y un único lenguaje de predicados que los lea y cruce relaciones. El resultado del paquete es GO04 (proyección, `source_hash`, `contract_signature`, staleness y filtros estructurados sin re-extraer Markdown) más GO05 (lenguaje unificado sobre esa proyección, con `where_parse` y `FieldCondition` como shims deprecados). Límites: PK02 no se ejecuta; termina cuando terminan sus hijos. No retira shims (GO10), no cambia deskops, no diseña la semántica ni la costura de backend (las recibe de GO02/GO03) y no persiste hechos derivados.

## AMBIGUEDADES  
ninguna.

## DRY-RUN  
PK02 no ejecutable: se cumpliría por sus hijos, en orden GO04 → GO05. GO04 recibiría el índice compuesto y la costura de GO03, más `G_SEAM`; leería shards, payloads, `__references__` y ejecutor de `StructuredQuery`; produciría la facet `payload`, `source_hash`, `contract_signature`, versión 5, staleness corregida y filtros estructurados, sin cambiar resultados existentes. Transferiría a GO05 la proyección y el índice ya versionado. GO05 recibiría además la gramática/semántica de GO02 y `G_SEMANTICS`; como primer paso capturaría goldens contra `where_parse` y `FieldCondition` posteriores a GO04; luego implementaría parser/evaluador, API única, avisos de deprecación y tests de equivalencia. Validación conjunta futura: tests existentes de `StructuredQuery` sin cambios; cero llamadas a `Validator.extract` en consulta estructurada y en `--where`; `any()/all()` desde CLI con explicación; aviso de shim probado; goldens de equivalencia verdes; shard v4 stale y reconstruido; CHANGELOG y documentación. Dependencias externas: GO02, GO03 y sus gates.

## FUTURO  
GO10 decidirá el retiro de shims. GO02 y GO03 producirán `G_SEMANTICS` y `G_SEAM`. El TaskDoc fijará archivos, tests y nombres exactos. El operador del desk aceptará la revisión en frío; deskops consumirá el resultado en su propio plan y `G_CONSUMER`.

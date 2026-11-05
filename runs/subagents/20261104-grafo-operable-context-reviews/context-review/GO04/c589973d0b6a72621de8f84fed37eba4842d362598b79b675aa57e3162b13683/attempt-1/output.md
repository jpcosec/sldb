## REFORMULACION
GO04 es un nodo de entrega (`kind: code`, `owner_repo: sldb`) del agregado PK02. Busca que cada nodo del índice de aristas lleve una facet `payload` plana (escalares y listas de escalares; anidados omitidos y documentados), con `content_hash` y `field_hashes`, respetando `__indexed__` si existe. Además corrige `EdgeIndex.stale`: el shard guarda `source_hash` y la firma de contrato del modelo, y se marca stale si cambia cualquiera. Sube `EDGE_INDEX_VERSION` de 4 a 5 y permite filtrar por la facet con `StructuredQuery`, sin cambiar resultados existentes ni usar el `eval` de GO03.

## AMBIGUEDADES
1. “Formato de shard: se agrega la clave payload al registro del nodo; nada más cambia” contradice “el shard guarda source_hash del documento y la firma de contrato del modelo”. Obliga a inventar si el formato solo admite `payload` o también esos dos campos nuevos.
2. “al abrir el store, un shard con versión menor se marca stale y se reconstruye en la siguiente reconstrucción (la próxima escritura o stores build)” frente a la aceptación “un shard de versión 4 se reconstruye al abrir y escribir”. Obliga a decidir si abrir solo marca stale o ya reconstruye.
3. “se omiten de la proyección y se documenta” no tiene ruta en `output_scope`, que no incluye `docs/architecture/`; la regla común 3 exige documentar allí toda capacidad nueva. Obliga a inventar dónde documentar o a exceder el alcance.
4. “La proyección se invalida por content_hash” frente a “stale cuando el source_hash del archivo difiere”. Obliga a decidir qué hash gobierna la invalidación y la reconstrucción.

## DRY-RUN
Un ejecutor leería `dag.yaml` (GO04, GO03, G_SEAM), el código de `edge_index`, `edge_sync`, `graph/executor.py`, `structural_queries.py`, modelos y tests. Cambiaría: constructor de facet con escalares, resolución de `__indexed__`, escritura de `payload`/`source_hash`/firma de contrato en shards, versión 5, lógica de stale y reconstrucción, filtros de `StructuredQuery` y su executor, tests de cero `Validator.extract`, mediciones y CHANGELOG. Depende de GO03/G_SEAM y de la metadata de modelos. Validaría con pytest: tests existentes de `StructuredQuery` sin cambios, edición externa del Markdown, cambio en `__references__`, shard v4, MB y número de shards antes/después.

## FUTURO
GO03 produce G_SEAM; GO05 consume la facet y la staleness; GO08 cablea `anchors check` en `stores check`; GO10 retira shims. Un humano acepta la revisión en frío y escribe la disposición en `reviews/rN.md`; otro promueve el nodo con `deskops add task --from-drawer`. Nada de esto es ambigüedad de GO04.

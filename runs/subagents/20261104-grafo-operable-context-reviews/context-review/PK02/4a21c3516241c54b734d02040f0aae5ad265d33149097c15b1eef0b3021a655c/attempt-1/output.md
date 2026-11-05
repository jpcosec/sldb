## REFORMULACION
PK02 es un agregado no ejecutable: no se promueve ni se ejecuta; termina cuando cierran GO04 y GO05. Su propósito es que el grafo tenga los campos proyectados y que exista un único lenguaje de predicados que los lea y cruce relaciones. Resultado: GO04 proyecta el payload a los nodos y corrige staleness; GO05 implementa el lenguaje de GO02 sobre esa proyección y reemplaza los dos lenguajes actuales. Repo dueño: `sldb`. Límites: no define la semántica (la fija GO02), no cambia el backend (costura de GO03), no toca deskops, no retira los alias viejos —los deja deprecados— y no promueve el agregado.

## AMBIGUEDADES
ninguna

## DRY-RUN
Hipotéticamente, un ejecutor futuro no ejecuta PK02: promueve GO04 y luego GO05.

GO04 recibe el índice de aristas existente, el `dirty set`, el `EDGE_INDEX_VERSION` y `G_SEAM` de GO03. Produce nodos con facet de payload, `content_hash` y `field_hashes`; staleness corregida para edición externa y nuevos campos de `__references__`; filtrado de `StructuredQuery` por payload; versión de índice incrementada; medición de tamaño antes/después. Transfiere a GO05 la proyección consultable y el índice stale-correcto.

GO05 recibe `G_SEMANTICS` de GO02, la proyección de GO04 y `G_SEAM` de GO03. Produce parser/evaluador único, caminos con cuantificadores y clausura, explicación estructurada, alias deprecados de `where_parse` y `FieldCondition`, tests de equivalencia verdes y los xfail de GO02 verdes. No transfiere a otro hijo de PK02.

Validación conjunta: GO04 y GO05 verdes; `--where` nuevo y consulta `any()/all()` sobre relación responden desde CLI con envelope y `--explain`; `where_parse` y `FieldCondition` emiten aviso de deprecación y pasan equivalencia; una consulta estructurada por campo y la evaluación masiva no llaman a `Validator.extract`; editar el Markdown por fuera marca stale y la reconstrucción actualiza; tamaño del índice medido y registrado.

## FUTURO
GO03 debe producir `G_SEAM` y la confirmación humana de D5; GO02 debe producir `G_SEMANTICS` y la confirmación de D6. GO01/G_BOUNDARY y los hijos de PK02 deben cerrar con tests verdes. Un humano confirma D5/D6 y acepta la revisión en frío; PK02 cierra por cierre de sus hijos.

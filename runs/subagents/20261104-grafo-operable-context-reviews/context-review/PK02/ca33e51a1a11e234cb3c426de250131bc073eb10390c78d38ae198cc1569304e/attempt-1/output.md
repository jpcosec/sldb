REFORMULACION

PK02 es un agregado no ejecutable: termina cuando terminan GO04 y GO05. Su encargo sustantivo es que el grafo de sldb tenga los campos del payload proyectados en los nodos y un único lenguaje de predicados que los lea y cruce relaciones. Repo dueño: sldb. GO04 proyecta el payload y corrige `EdgeIndex.stale`; GO05 implementa el lenguaje de GO02 sobre esa proyección y deja `where_parse` y `FieldCondition` como shims deprecados que avisan. Límite: no retira los shims; eso es GO10, en PK04. Resultado conjunto: `--where` nuevo sin re-extraer Markdown, consultas con `any()`/`all()` desde CLI con explicación, shims funcionando con aviso probado y tests de equivalencia contra goldens de los parsers viejos.

AMBIGUEDADES

1. «los tests de equivalencia comparan el resultado nuevo con goldens capturados con los parsers viejos antes del cambio». No queda fijado si «antes del cambio» significa antes de GO05 o antes de que GO04 modifique `structural_queries.py` y el executor, que están en su `output_scope`. Obligaría a inventar a qué nodo pertenece la captura de goldens y si GO04 debe preservar o congelar el comportamiento viejo para que los goldens sigan siendo válidos.

DRY-RUN

Hipotético, sin ejecutar. Orden por dependencias: GO04 y luego GO05.

GO04 lee el índice de aristas, modelos y la costura de GO03; agrega `payload`, `content_hash` y `field_hashes` al shard, sube `EDGE_INDEX_VERSION` a 5, hace stale por `source_hash` y firma de contrato, y habilita filtros estructurados sobre `payload`. Entrega a GO05 nodos con campos proyectados y staleness corregida; valida con tests de proyección, edición externa, campo nuevo en `__references__`, cero `Validator.extract` y mediciones de tamaño/shards.

GO05 lee la spec y tests xfail de GO02 y la proyección de GO04; captura goldens con los parsers actuales, implementa parser/evaluador, shims con `DeprecationWarning` y entrada en `warnings`, y `--explain`. Entrega API única detrás de `where_matches`, `edges_holding`, `StructuredQuery` y `--where`; valida spec, equivalencia, consulta CLI con `any()`/`all()`, cero extracción y aviso probado.

Validación conjunta: correr la aceptación de PK02 sobre ambos hijos, comprobar goldens, avisos de shims, consulta CLI explicada y mediciones registradas en Validation y CHANGELOG.

FUTURO

GO03 debe producir `G_SEAM` y GO02 `G_SEMANTICS`; sin esos gates el paquete no arranca. GO10/PK04 retira los shims. El consumo por deskops pertenece a su propio plan.

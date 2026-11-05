## REFORMULACION

Propósito: dotar al índice de aristas de los campos del payload y de un único lenguaje de predicados que los lea y cruce relaciones. Resultado del paquete: `--where` nuevo evalúa sin re-extraer Markdown; una consulta con `any()/all()` sobre una relación responde desde la CLI con explicación; `where_parse` y `FieldCondition` quedan deprecados con aviso probado y tests de equivalencia. Repo dueño: sldb. Límites: no toca deskops ni introduce backend externo; es agregado, no se ejecuta y termina cuando terminan GO04 y GO05.

## AMBIGUEDADES

1. "where_parse y FieldCondition marcados deprecados con aviso probado" (aceptación PK02) frente a "los parsers viejos se borran" (scope GO05) y "se marca deprecado y se retira en un nodo explícito, no de paso" (alcance, regla 4). Obliga a inventar si `where_parse` sobrevive como shim que avisa o se elimina ya.
2. "tests de equivalencia" (aceptación PK02) frente a "los parsers viejos se borran" (scope GO05). Obliga a inventar cómo se ejecuta el camino viejo tras el borrado: goldens previos, ejecución antes de borrar o comparación contra la tabla de GO02.

## DRY-RUN

Hipotético, sin ejecutar. GO04 parte de G_SEAM (GO03) y del índice compuesto; añade la clave `payload` al registro del nodo, sube `EDGE_INDEX_VERSION` a 5, corrige `stale` por `source_hash` y `__references__`, y habilita filtros de `StructuredQuery` sobre la facet. Transfiere a GO05 la facet poblada y el backend con `eval` de un documento. GO05 parte de G_SEMANTICS (GO02) y de GO04; implementa parser y evaluador, caminos con `any/all/none/count`, clausura, `incomplete` y explicación; adapta `FieldCondition`, emite `DeprecationWarning`/alert y expone `--where` y API única. Validación conjunta: `--where` con `any()/all()` desde CLI y `--explain`; test de cero `Validator.extract`; captura de aviso; equivalencia; CHANGELOG y docs.

## FUTURO

GO03 produce G_SEAM y GO02 produce G_SEMANTICS; el dueño confirma D5 y D6. El retiro efectivo de la sintaxis vieja queda para un nodo explícito posterior.

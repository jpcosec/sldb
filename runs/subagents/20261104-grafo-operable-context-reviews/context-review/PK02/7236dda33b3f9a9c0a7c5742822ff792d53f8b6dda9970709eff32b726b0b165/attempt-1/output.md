## REFORMULACION

PK02 “Sustrato” es un agregado no ejecutable del repo sldb. Su resultado sustantivo: que el índice de aristas proyecte campos escalares del payload en cada nodo, detecte staleness por `source_hash` y firma de contrato, y que exista un único lenguaje de predicados que lea esa proyección, cruce relaciones y conserve `where_parse` y `FieldCondition` como shims deprecados con aviso. Límites: no define semántica (GO02), no implementa backend (GO03) ni retira shims (GO10); no autentica actores, no persiste hechos derivados y no toca deskops. Termina cuando terminan GO04 y GO05.

## AMBIGUEDADES

ninguna

## DRY-RUN

No se ejecuta PK02: se promueven y ejecutan sus hijos.

GO04 lee GO03/`G_SEAM`, el índice actual, modelos y `StructuredQuery`; cambia `edge_index`, `edge_sync`, `facet_match`, `executor` y `structural_queries`; produce facet `payload`, `field_hashes`, `source_hash`, `contract_signature`, `EDGE_INDEX_VERSION=5`, staleness por `source_hash` o firma de contrato y filtros estructurados sin re-extraer Markdown. Entrega a GO05 nodos con payload proyectado y staleness corregida.

GO05 lee GO02/`G_SEMANTICS`, el backend de GO03, la proyección de GO04 y los dos lenguajes actuales; primero captura goldens con el estado posterior a GO04; luego implementa parser/evaluador, shims con `DeprecationWarning` y entrada en `warnings` del envelope, CLI `--where`/`--explain`, tests de equivalencia y xfail verdes. Entrega el lenguaje único.

Validación conjunta: cero `Validator.extract` en `--where` y en consulta estructurada; `any()/all()` desde CLI con explicación; shims avisan y la vía nueva no; goldens equivalentes; tests existentes pasan; CHANGELOG y docs actualizados. Dependencias: GO04←GO03; GO05←GO02, GO04. Gates `G_SEAM` y `G_SEMANTICS`.

## FUTURO

GO10 retira los shims en PK04. deskops consume el resultado mediante `G_CONSUMER`. El operador del desk dispone la revisión en frío y el dueño indica el host de pytest.

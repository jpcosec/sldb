## REFORMULACION
PK02 (Sustrato) es un agregado no ejecutable del repo `sldb`: su encargo es que el grafo tenga campos proyectados y que exista un único lenguaje de predicados que los lea y cruce relaciones. El resultado sustantivo del paquete es: `--where` nuevo evalúa sin re-extraer Markdown; una consulta con `any()`/`all()` sobre una relación responde desde la CLI con explicación; `where_parse` y `FieldCondition` siguen funcionando como shims que avisan, con tests de equivalencia contra goldens capturados primero por GO05 sobre las implementaciones viejas posteriores a GO04. Límites: el agregado no se promueve; se promueven GO04 y GO05. No se retiran los shims (eso es GO10), no se persisten hechos derivados, no hay auth, motor externo ni cambios en deskops; GO04 no cambia el resultado de consultas existentes.

## AMBIGUEDADES
ninguna

## DRY-RUN
Hipotético, sin ejecutar. PK02 no se ejecuta: termina cuando terminan GO04 y GO05, en ese orden por `GO05 depends_on GO04`.

GO04 lee el índice de aristas, modelos, `__references__`, `StructuredQuery` y su executor; requiere GO03 y `G_SEAM`. Cambia: agrega la facet `payload` a los nodos, sube `EDGE_INDEX_VERSION` de 4 a 5, corrige staleness por `source_hash` y firma de contrato, y permite filtros estructurados sobre `payload`. Transfiere a GO05 la proyección por nodo y la garantía de que las consultas existentes no cambian.

GO05 lee la spec de GO02, la proyección de GO04 y el backend de GO03; requiere `G_SEMANTICS` y `G_SEAM`. Primero captura goldens contra `where_parse` y `FieldCondition` posteriores a GO04; luego implementa parser/evaluador, deja ambos como shims con `DeprecationWarning` y aviso en el envelope, y unifica la API tras `where_matches`, `edges_holding`, `StructuredQuery` y `--where`. Transfiere el lenguaje único con tests de equivalencia.

Validación conjunta: `--where` sin llamadas a `Validator.extract`; `any()`/`all()` sobre relación con explicación; shims que avisan y equivalen a goldens; tests existentes de `StructuredQuery` sin cambios; reconstrucción de shards versión 4 a 5 y casos de staleness; medidas de índice en Validation y CHANGELOG.

## FUTURO
GO10 retira los shims en PK04. GO02 produce `G_SEMANTICS`; GO03 produce `G_SEAM` y el backend. El operador del desk de `sldb` escribe la disposición en `reviews/rN.md`; el dueño indica el host de pytest. deskops producirá `G_CONSUMER` en su propio plan.

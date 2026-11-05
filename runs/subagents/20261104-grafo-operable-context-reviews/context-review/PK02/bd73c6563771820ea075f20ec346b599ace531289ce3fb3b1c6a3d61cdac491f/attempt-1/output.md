## REFORMULACION

**Propósito:** dotar al grafo de sldb de un sustrato consultable: proyectar el payload en los nodos del índice y disponer de un único lenguaje de predicados que lea esos campos y cruce relaciones.

**Resultado:** PK02 entrega (a) nodos con facet `payload`, `field_hashes`, `source_hash` y `contract_signature`, staleness corregida por `source_hash`/`contract_signature`, `EDGE_INDEX_VERSION = 5` y filtros `StructuredQuery` sobre la proyección sin re-extraer Markdown; y (b) el lenguaje de GO02 implementado sobre esa proyección, con booleanos, caminos, cuantificadores, clausura, `incomplete` y explicación, dejando `where_parse` y `FieldCondition` como shims deprecados que avisan. El retiro de shims es GO10, fuera de PK02.

**Repo dueño:** sldb. **Límites:** no retira shims, no autentica actores, no persiste hechos derivados y no cambia el resultado de consultas existentes. **Dependencias:** GO04 depende de GO03/G_SEAM; GO05 de GO02/G_SEMANTICS/G_SEAM. PK02 es agregado no ejecutable: termina cuando terminan GO04 y GO05.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **GO04 (primero):** leería `edge_index`, `edge_sync`, `compose`, `facet_match`, `executor`, `structural_queries`, `graph-backend.md` y CHANGELOG. Produciría la proyección, las firmas de contrato, la invalidación por `source_hash`/`contract_signature` y los filtros estructurados. Transferiría a GO05 la facet `payload` disponible, staleness corregida, versión 5 y consultas sin re-extracción.
- **GO05 (después):** recibiría la proyección de GO04 y la spec de GO02; capturaría goldens con `where_parse`/`FieldCondition` tal como quedan tras GO04; implementaría parser/evaluador, API única, shims con `DeprecationWarning`, `--where` nuevo, `--explain` y warnings de envelope para filtros dict. Transferiría el lenguaje único y la equivalencia contra goldens.
- **Validación conjunta:** tests de GO04 (stale por edición externa y por `__references__`, cero `Validator.extract`, versión 5, tamaños) más tests de GO05 (spec GO02, equivalencia, `any()`/`all()` por CLI, cero extracción, avisos) deben satisfacer la aceptación de PK02.

## FUTURO

GO10/PK04 retira los shims. GO03 produce `G_SEAM`; GO02 produce `G_SEMANTICS`. La revisión en frío humana acepta o dispone. La promoción fija nombres exactos y tests en el TaskDoc. deskops consumirá el resultado en su propio plan (`G_CONSUMER`).

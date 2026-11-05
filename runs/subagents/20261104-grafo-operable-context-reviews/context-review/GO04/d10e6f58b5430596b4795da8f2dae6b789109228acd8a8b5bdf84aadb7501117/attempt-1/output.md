# REFORMULACION

Encargo de GO04: que cada nodo de documento del índice de aristas lleve una facet `payload` plana (campos escalares o listas de escalares, con omisión de anidados), más `content_hash` y `field_hashes`; shards v5 con `payload`, `source_hash` y `contract_signature`; staleness gobernada por `source_hash` o firma de contrato (incluido cambio en `__references__`), y filtros de `StructuredQuery` sobre la facet sin re-extraer Markdown. Repo dueño: sldb. Nodo `delivery`, no agregado, depende de GO03 y requiere `G_SEAM`. Límites: no cambia resultados existentes, no implementa el `eval` de GO03 ni el lenguaje de GO05.

# AMBIGUEDADES

1. "Más content_hash y field_hashes." frente a "se agregan tres claves al registro del nodo, payload, source_hash y contract_signature". Obliga a inventar dónde viven `content_hash` y `field_hashes`: ¿dentro de `payload`, como claves separadas, o ya existentes?
2. "fields: nombres de campo ordenados" en la firma. Obliga a inventar si son todos los campos del modelo o solo los `__indexed__`/proyectados.
3. No se define qué devuelve un filtro `StructuredQuery` sobre un campo omitido de la proyección (dict o lista anidada). Obliga a inventar (¿vacío, error, re-extracción?).

# DRY-RUN

Lecturas: spec de modelos, código de shards/`compose`, `edge_sync`, `executor`, `structural_queries`, modelo base, inbox 20261102-065705. Cambios previstos: proyección al construir shard; añadir `payload`, `source_hash`, `contract_signature`; `EDGE_INDEX_VERSION=5`; marca stale por versión/source_hash/firma; `facet_match.py`; filtros en executor y `structural_queries`; sección en `graph-backend.md`; CHANGELOG. Dependencias: GO03 (costura y argumento de proyección), `G_SEAM` aún `pending`. Validaciones futuras: edición externa marca stale; campo nuevo en `__references__`; consulta por `status` con cero `Validator.extract`; shard v4 stale y reconstruido; tests existentes verdes; MB y nº de shards antes/después en Validation y CHANGELOG.

# FUTURO

GO05 consume la facet y produce el lenguaje; GO07 añade `<campo>__anchor_state`; GO08 cablea `stores check`. El TaskDoc fijará nombres exactos de archivos y tests; el dueño/host robocop2 corre pytest y confirma `G_SEAM`.

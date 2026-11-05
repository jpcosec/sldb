REFORMULACION
GO04 es un encargo de planificación `code` en sldb. Propósito: que el índice de aristas exponga los campos de payload de cada documento para consultarlos sin reextraer Markdown y que la detección de staleness cubra ediciones externas y nuevos campos de `__references__`. Resultado: facet payload con `content_hash` y `field_hashes`, invalidación/reconstrucción por hash y dirty set, `EDGE_INDEX_VERSION` incrementada, filtrado de `StructuredQuery` por campos y arreglo de `EdgeIndex.stale`. Repo dueño: sldb. Límites: solo campos escalares y listas de escalares (o `__indexed__`), cambios de formato de shards “más de lo necesario” no definidos, `output_scope` acotado a `edge_index`, `edge_sync` y `facet_match`; depende de GO03 y del gate G_SEAM.

AMBIGUEDADES
1. “o los que el modelo declare en `__indexed__`”: no se define cómo se declara `__indexed__` ni si reemplaza o amplía el conjunto por defecto. Obliga a inventar sintaxis, precedencia y tratamiento de modelos sin declaración.
2. “entran al nodo del índice de aristas como facet payload”: no se especifica la forma del facet payload (nombres, anidamiento, tipos, compatibilidad con shards). Obliga a inventar el contrato de representación.
3. “Sin cambiar el formato de los shards más de lo necesario”: “necesario” no tiene criterio. Obliga a inventar el umbral de cambio permitido y puede habilitar exceder el alcance.
4. “tamaño del índice medido antes y después en este repo y registrado”: no dice dónde se registra ni en qué unidad/formato. Obliga a inventar el artefacto de evidencia; la aceptación deja de ser comprobable.

DRY-RUN
Lecturas: contrato de GO03/G_SEAM, código de edge_index/edge_sync/StructuredQuery, formato actual de shards y la nota 20261102-065705. Cambios previstos dentro del `output_scope`: añadir facet payload y versión; invalidar por hash; corregir stale para edición externa y `__references__`; permitir filtro por payload en `StructuredQuery`. Dependencias: GO03 y confirmación de D5/G_SEAM; sin contrato, registrar hipótesis y no inventar API. Validaciones futuras: escritura expone campos; edición externa marca stale y reconstruye; consulta por `status = closed` sin `Validator.extract`; medición de tamaño antes/después. No se ejecuta nada.

FUTURO
GO03 produce G_SEAM y el dueño confirma D5; GO05 consume la proyección para el lenguaje; GO07 consume campos/anclas; PK02 cierra cuando GO04 y GO05 terminan. La aceptación del nodo y la revisión en frío son humanas.

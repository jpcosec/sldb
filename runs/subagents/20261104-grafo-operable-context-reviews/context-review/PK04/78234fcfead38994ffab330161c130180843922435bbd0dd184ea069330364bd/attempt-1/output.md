## REFORMULACION
PK04 es un agregado no ejecutable: su encargo es que sldb evalúe reglas “cuando importa”, convierta la transición en datos de la arista y retire los lenguajes viejos. Resultado sustantivo: un paquete en serie donde GO09 traslada el efecto de transición a `RelationDoc.attributes` y expone `effects` en `edges_holding`; GO08 añade `findings`, evaluación `on_write`/`on_transition`/`on_check`, caché derivada y validación de condiciones; GO10 elimina los shims `where_parse` y `FieldCondition`. Repo dueño: sldb. Límite: el agregado no se promueve ni ejecuta; se promueven sus hijos. Frontera declarada: “GO09 es dueño de la clave effects, GO08 de la clave findings”.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro no ejecutaría PK04: leería `dag.yaml`, brief, alcance, decisiones y TaskDocs de GO05, GO06, GO07, GO09, GO08 y GO10; comprobaría gates y promovería cada hijo por separado.

1. GO09: entra con GO05 y `G_SEAM`; produce convención de `attributes`, validación en `relation_doc.py`, `effects` en `edges_holding`, `apply_effects` y documentación. Entrega a GO08 un resultado con `effects` estable.
2. GO08: entra con GO06 (`RuleDoc`), GO07 (anclas), GO09 (`effects`) y `G_OPS_PREREQ`; produce `findings`, `blocked`, evaluación en escritura/transición/check, caché en `.sldb_cache`, validación de condiciones y el ejemplo end-to-end. No modifica `effects`. Entrega a GO10 el lenguaje único ya en uso.
3. GO10: entra con GO02 y GO08; retira shims y reescribe documentación, conservando goldens como tests del lenguaje nuevo.

Validación conjunta: suite completa verde en el host indicado; escritura con regla `error` rechazada sin persistir; `alert` no falla; `edges_holding` devuelve `effects` y `findings` separados; `edges check` valida condiciones; pasa el ejemplo end-to-end; grep confirma ausencia de `where_parse` y `FieldCondition`.

## FUTURO
GO05, GO06 y GO07 producen contratos previos; GO02 produce `G_SEMANTICS`; otros nodos o gates producen `G_SEAM` y `G_OPS_PREREQ`. Deskops producirá `G_CONSUMER`. La persona que opera el desk de sldb acepta la revisión en `reviews/rN.md` e indica el host de validación; la promoción fija TaskDocs y archivos.

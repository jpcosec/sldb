REFORMULACION

PK04 es un agregado no ejecutable del plan `grafo-operable`, repo dueño `sldb`. Propósito: que las reglas se evalúen cuando importan (escritura, transición, check), que la máquina de estados sea enteramente datos en las aristas y que los lenguajes viejos de condición se retiren. Resultado del paquete: GO09 lleva `sets`/`terminal` a `RelationDoc.attributes` y agrega `effects` a `edges_holding`; GO08 agrega `findings` al mismo resultado y evalúa `on_write`/`on_transition`/`on_check` con caché por dirty set y punto fijo; GO10 elimina `where_parse` y `FieldCondition` y sus menciones. Límites: frontera `effects` (GO09)/`findings` (GO08) en `edges_holding`; hechos derivados nunca persistidos; sin auth, sin motor externo y sin tocar deskops; la evaluación no juzga calidad.

AMBIGUEDADES

Ninguna. Las dependencias externas al paquete (GO05, GO06, GO07) y los gates (`G_SEAM`, `G_OPS_PREREQ`) están declarados en `dag.yaml`; no obligan al ejecutor a inventar.

DRY-RUN

GO09 (entradas: lenguaje de GO05, gate `G_SEAM`; salida: convención de `attributes`, `effects` resueltos, `apply_effects` y tests) → GO08 (entradas: `RuleDoc` de GO06, anclas de GO07, `effects` de GO09, gate `G_OPS_PREREQ`; salida: `findings` junto a `effects`, rechazo en `on_write`, bloqueo en `on_transition`, `stores check`, validación en `edges check`, test end-to-end y medición) → GO10 (entrada: GO08 y llamantes ya migrados; salida: borrado de shims y menciones, suite verde, CHANGELOG). Validación conjunta: tests de GO09 y GO08 verdes; el test end-to-end de GO08 en sus tres pasos; escritura que viola regla `error` rechazada y `alert` persistida; `effects` y `findings` en claves separadas; `edges check` falla ante condición mal formada; grep final sin `where_parse`/`FieldCondition` salvo CHANGELOG. Nada se ejecuta aquí.

FUTURO

GO05, GO06 y GO07 deben cerrar antes; el dueño o el gate desbloquean `G_SEAM` y `G_OPS_PREREQ`; el operador del desk acepta la revisión en `reviews/rN.md`; el TaskDoc fijará archivos y tests exactos; deskops verificará el consumo en `G_CONSUMER`; el dueño indica el host de pytest (robocop2 en esta serie).

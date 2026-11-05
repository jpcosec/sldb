REFORMULACION
Propósito: que sldb evalúe reglas cuando importa —escritura, transición y check—, que la máquina de estados sea datos en las aristas y que los lenguajes viejos se retiren. Resultado: GO09 lleva sets/terminal a RelationDoc.attributes y añade effects a edges_holding; GO08 evalúa on_write/on_transition/on_check, añade findings y blocked, cablea anclas doc:, caché por dirty set y punto fijo, y valida condiciones en edges check; GO10 elimina where_parse y FieldCondition. Repo: sldb. Límites: PK04 es agregado no ejecutable; termina cuando terminan GO09, GO08 y GO10. Frontera: GO09 dueño de effects; GO08 de findings, sin tocar effects. Nada derivado se persiste; sin auth ni motor externo; no se toca deskops salvo la nota permitida.

AMBIGUEDADES
1. «GO08 ... evalúa en escritura, transición y check» frente a «edges check valida condiciones». «check» no se identifica: el contrato de GO08 lo ata a stores check, pero el acceptance nombra edges check. Obliga a inventar si las reglas también corren en edges check o si allí solo se parsean condiciones.
2. «where_parse y FieldCondition ya no existen» frente a la excepción histórica que conserva el contrato de GO10. Obliga a decidir si el agregado cierra con esa tabla en docs/ o si «existir» la incluye; sin esa regla, la validación conjunta puede fallar con todos los hijos verdes.

DRY-RUN
GO09: entran GO05 y G_SEAM; salen convención attributes, effects resueltos y apply_effects. Transfiere a GO08 effects estable.
GO08: entran GO06, GO07 y GO09; salen evaluación en los tres momentos, findings/blocked, caché .sldb_cache, edges check parseando, ejemplo end-to-end y medición. Transfiere a GO10 API única en uso y shims aún presentes.
GO10: entran GO02 y GO08; salen shims borrados, docs reescritos y goldens conservados.
Validación conjunta: pytest completo; ejemplo end-to-end en tres pasos; escritura error rechazada y alerta persistida; effects/findings en claves separadas; edges check falla condición mal formada; grep de retiro; medición y CHANGELOG. G_SEAM y G_OPS_PREREQ los satisfacen otros/humano.

FUTURO
GO05 entrega lenguaje/backend; GO06 RuleDoc; GO07 anclas; deskops consume en G_CONSUMER; el operador de sldb acepta la revisión en reviews/rN.md; el dueño confirma gates y host de pytest. No son ambigüedades de PK04.

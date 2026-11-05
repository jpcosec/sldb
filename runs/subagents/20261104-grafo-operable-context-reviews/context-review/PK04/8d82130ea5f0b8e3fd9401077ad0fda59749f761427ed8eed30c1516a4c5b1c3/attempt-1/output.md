**REFORMULACION**  
PK04 es un agregado no ejecutable del plan `grafo-operable`, repo `sldb`. Su encargo: que las reglas se evalúen al escribir, transicionar y comprobar; que el efecto de una transición viva como datos en la arista; y que se retiren `where_parse` y `FieldCondition`. Resultado conjunto: `edges_holding` devuelve `effects` y `findings` en claves separadas; una escritura con regla `error` se rechaza con explicación y una `alert` no falla; `edges check` valida condiciones; pasa el end-to-end de GO08; los lenguajes viejos desaparecen. Límites: el agregado no se promueve; no hay ejecución autorizada; GO09 posee `effects`, GO08 `findings`; no autentica actores ni produce hechos externos.

**AMBIGUEDADES**  
1. “GO08 ... evalúa en escritura, transición y check ... Una escritura que viola una regla error es rechazada con explicación”. Solo se define el rechazo en escritura; no se dice si un finding `error` en `on_transition` bloquea la transición ni si `on_check` altera el exit. Obligaría a inventar la semántica de severidad fuera de `on_write`.

**DRY-RUN**  
Hipotético, sin ejecutar. PK04 termina cuando terminan sus hijos.  
- GO09: lee GO05 y `RelationDoc`; cambia `edges_holding` y `apply_effects`; entrega a GO08 la convención `attributes`, `effects` resueltos y la frontera de claves. Requiere `G_SEAM`.  
- GO08: lee GO09, GO06, GO07 y GO05; cambia guardado de payload, `edges_holding`, `stores check` y `edges check`; entrega a GO10 llamantes migrados, findings y suite con el end-to-end. Requiere `G_OPS_PREREQ`.  
- GO10: lee GO08 y los llamantes ya migrados; borra shims; entrega grep limpio salvo CHANGELOG, suite verde y retiro registrado.  
Validación conjunta: ejecutar la aceptación de PK04 —rechazo/alertas, claves separadas, `edges check`, integración de GO08 y ausencia de `where_parse`/`FieldCondition`— sin ejecutar ahora.

**FUTURO**  
`G_CONSUMER` lo produce deskops al verificar que puede retirar `sets_status`/`terminal`; `G_SEAM` y `G_OPS_PREREQ` condicionan hijos. El dueño decide promoción, host de pytest y versión de CHANGELOG. No son ambigüedades.

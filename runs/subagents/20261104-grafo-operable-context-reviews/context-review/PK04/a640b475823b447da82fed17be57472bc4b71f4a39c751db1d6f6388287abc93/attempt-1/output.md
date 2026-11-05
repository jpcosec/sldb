## REFORMULACION
PK04 es un agregado no ejecutable del plan grafo-operable; su propósito es que las reglas se evalúen cuando importa y que la máquina de estados sea enteramente datos. Resultado: GO08 aporta evaluación `on_write`/`on_transition`/`on_check`, incremental y a punto fijo; GO09 lleva el efecto de una transición a `RelationDoc.attributes`; ambos convergen en `edges_holding`. Repo dueño: sldb. Límites: no se promueve el agregado, solo sus hijos; no hay arista entre GO08 y GO09; termina cuando ambos terminan. Aceptación conjunta: escritura con regla error rechazada con explicación, alerta no falla, `edges_holding` devuelve efectos desde attributes, `edges check` valida condiciones y el ejemplo end-to-end de ROOT pasa como integración.

## AMBIGUEDADES
1. «Sin arista entre ambos; convergen en edges_holding con output_scope delimitado.» No fija la frontera de cambios ni el contrato combinado en `edges_holding` (findings y effects) pese a que ambos hijos lo tocan; obligaría a inventar quién modifica qué, en qué orden se integra y cómo se compone la salida.
2. «el ejemplo end-to-end de ROOT pasa como test de integración.» El input de PK04 no define ese ejemplo ni su criterio de «pasa»; obligaría a inventar caso, datos y aserciones si ROOT no lo entrega.

## DRY-RUN
Hipotético, sin ejecutar. GO08 recibiría RuleDoc de GO06, anclas de GO07, G_OPS_PREREQ y los puntos actuales de guardado/consulta; produciría rechazo/aceptación en escritura, findings `on_transition` y `on_check`, caché por `content_hash`, validación de condiciones y test de integración. GO09 recibiría GO05/G_SEAM y la convención de atributos; produciría effects resueltos en `edges_holding`, `apply_effects` puro y documentación. No hay entrega directa entre hermanos: comparten `edges_holding` y el resultado se valida al final ejecutando ambos conjuntos de tests y la aceptación del agregado: rechazo/alertas, findings y effects juntos, `edges check`, ejemplo ROOT y medición. GO08 podría ir antes por construir evaluación; GO09 después para integrar effects, pero el orden no es contractual.

## FUTURO
GO06/GO07 entregan contratos a GO08; GO05/G_SEAM a GO09. Un humano confirma D5–D7 y G_OPS_PREREQ; deskops valida en G_CONSUMER que puede retirar `sets_status`/`terminal`. La promoción de hijos y los nombres exactos de archivos/tests quedan al TaskDoc. ROOT debe aportar el ejemplo end-to-end.

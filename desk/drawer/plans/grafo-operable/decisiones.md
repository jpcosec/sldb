# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. Una recomendación aceptada tácitamente se marca como tal; no se la hace pasar por decisión explícita.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| D1 | sldb se modifica a fondo para evaluar reglas sobre documentos, aristas y hashes ("operativicemos esto lo más posible en sldb; si hay que modificarlo a fondo, démosle"). La pill `pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops` se reescribe: evaluador genérico en sldb, reglas autoradas fuera. | Dueño | Chat de la sesión de deskops, 2026-11-04; pill editada con `deskops edit pill` | 2026-11-04 |
| D2 | Los gates de activación de una tarea son bloqueo duro, sin bandera de salto. La vía de escape es especializar tipos de tarea (`task.refactor` ≠ `task.debug`), cada tipo con sus gates. | Dueño | Respuesta a la pregunta "qué tan duro debe ser" | 2026-11-04 |
| D3 | No hay coordinación central entre desks: cada desk tiene sus tareas y pide feedback al resto. Scion coordina ejecución; deskops coordina conocimiento. | Dueño | Respuesta a la pregunta "quién acepta la disposición" | 2026-11-04 |
| D4 | El revisor barato bajo Scion sigue siendo pi deepseek, con bundle propio en el fork. | Dueño | Respuesta a la pregunta sobre el harness del revisor | 2026-11-04 |
| D5 | No saltar a Neo4j ahora: costura `GraphBackend` con networkx (ya dependencia de sldb) en proceso; otro motor entra detrás de la misma costura si hace falta. Reglas independientes del backend. | Dueño | Pregunta explícita en el chat de la sesión; respuesta "Sí, networkx tras la costura" | 2026-11-04, confirmada |
| D6 | Semántica del lenguaje de reglas: subconjunto de Datalog estratificado (sin funciones más allá de comparaciones, negación estratificada, mundo cerrado por store), para que kimun pueda adoptar reglas y recibos sin traducirlos. | Dueño | Pregunta explícita en el chat; respuesta "Sí" a Datalog estratificado con `incomplete` en el borde de links | 2026-11-04, confirmada |
| D7 | sldb no construye autenticación de actores; identidad viene de git y de la capa de ejecución. | Dueño | Pregunta explícita en el chat; respuesta "Sí" | 2026-11-04, confirmada |
| D8 | kimun no absorbe sldb v1 todavía: migra documentos, no al consumidor (deskops es escritor y kimun abandonó el round-trip estricto; sin cliente Python; modelos en rediseño; capa G bloqueada por D0 y D-G). Criterios para revisarlo: D0 y D-G decididos, spec 16 implementada, camino de escritura con round-trip, cliente o envelope estable, equivalente de condiciones por arista, `migrate` limpio en los cuatro desks. | Hecho verificado por el asistente, aceptado por el dueño al autorizar el plan sobre sldb v1 | Informe sobre kimun, 2026-11-04 | 2026-11-04 |

## Pendientes del dueño

- D5, D6 y D7 confirmadas el 2026-11-04 (tres preguntas explícitas, tres "Sí"). Sin pendientes de decisión para PK01.
- Las decisiones ya registradas en el Board de sldb que condicionan la operación (journal congelado; `.sldb` versionado y `.sldb_cache` ignorado) siguen en sus tareas; este plan no las reabre.

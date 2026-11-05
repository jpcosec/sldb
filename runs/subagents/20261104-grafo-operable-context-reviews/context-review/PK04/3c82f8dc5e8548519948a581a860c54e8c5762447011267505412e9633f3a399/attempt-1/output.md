REFORMULACION
PK04 es un agregado no ejecutable: encarga operativizar en sldb la evaluación de reglas. Propósito: evaluar reglas en escritura, transición y check, llevar el efecto de una transición a la arista y retirar los lenguajes viejos. Resultado: paquete de GO09, GO08 y GO10 en serie; frontera en `edges_holding`: GO09 dueño de `effects`, GO08 de `findings`. Repo: sldb. Límites: no se promueve el agregado; termina cuando terminan sus hijos; no incluye autenticación, motor externo ni cambios en deskops.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético, sin ejecutar. PK04 no corre: se promueven sus hijos. Lecturas: contratos de GO05, GO06, GO07 y los propios hijos. GO09 recibe GO05 y G_SEAM; documenta `sets`/`terminal` en `RelationDoc.attributes`, agrega `effects` a `edges_holding` y `apply_effects`; entrega `effects` resueltos, validación y docs. GO08 recibe GO06, GO07, GO09 y G_OPS_PREREQ; consume `effects` sin tocarla, agrega `findings` y `blocked`, evalúa `on_write`/`on_transition`/`on_check`, caché por dirty set, ejemplo end-to-end y medición; entrega `findings` y evaluación. GO10 recibe GO02 y GO08; retira shims, reescribe docs y conserva goldens; entrega grep limpio y suite. Validación conjunta: acceptance de PK04; `effects` y `findings` en claves separadas; `edges check` valida condiciones; el ejemplo end-to-end pasa; `where_parse` y `FieldCondition` ausentes; suite verde y CHANGELOG.

FUTURO
Humano/otro nodo: promover cada hijo con TaskDoc y preflight; fijar la lista exacta de grep en GO10; registrar la medición de GO08; deskops produce G_CONSUMER y verifica el retiro de `sets_status`/`terminal`. La disposición de revisión la escribe quien opera el desk de sldb.

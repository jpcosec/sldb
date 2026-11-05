## REFORMULACION

PK03 es un agregado no ejecutable del plan `grafo-operable`, repo dueño `sldb`; termina cuando terminan GO06 y GO07. Encarga dos capacidades: reglas como documentos (`RuleDoc`, `rules check`/`rules explain`) y anclas a documentos con hash de contrato (`doc:Model:name@sha256:<hash>`, estados `intact/changed/lost`, pinneado al guardar, `anchor_state` consultable desde reglas). Resultado sustantivo: un documento con `__doc_anchors__` queda consultable por `anchor_state`, y `rules check` reporta findings con severidad y cláusula fallida. Límites: sldb no define modelos de recibo, no autentica actores ni produce hechos externos; el cableado de `stores check` corresponde a GO08.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Hipotético, sin ejecutar. PK03 no se promueve ni ejecuta: se ejecutan sus hijos. GO06 entra tras GO05: recibe el lenguaje de predicados y define `RuleDoc`, validación al escribir, `rules check` y `rules explain`; sale con modelo, API/CLI de reglas, docs y CHANGELOG. GO07 entra tras GO04 y GO05: recibe la facet `payload` y el lenguaje; define ancla `doc:`, pinneado, estados, `check_doc_anchors`, extensión de `anchors check`, `Provenance` y entrada derivada `<campo>__anchor_state`; sale con API/CLI, modelo base, pasos de guardado, proyección, docs y CHANGELOG. GO06 y GO07 son hermanos sin arista: no se transfieren artefactos directamente; comparten prerrequisitos. Validación conjunta: aceptación de PK03 exige `rules check` con severidad/cláusula, `anchors check` con `intact/changed/lost`, y en GO07 una regla sobre `anchor_state` con `Review` pinneada a `Task`; eso ejercita ambos resultados. No reviso bloques `edge`.

## FUTURO

GO08 cablea `check_doc_anchors` en `stores check`; GO10 retira shims; deskops consume reglas/anclas en su propio plan y produce `G_CONSUMER`; el humano operador de sldb escribe la disposición en `reviews/rN.md`.

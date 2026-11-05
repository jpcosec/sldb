REFORMULACION

PK03 es un agregado del plan `grafo-operable`, repo dueño `sldb`. Su propósito es habilitar reglas como documentos y anclas a documentos con hash de contrato. El resultado sustantivo del paquete es: `RuleDoc` con sujeto por familia de modelo, condición, severidad y momento; `rules check`/`rules explain` con findings y explicación de cláusula fallida; y anclas `doc:` con pinneado por hash de contrato, estados `intact/changed/lost`, `anchors check`, integración en `stores check` y `anchor_state` consultable desde el lenguaje. Límites: no define modelos de recibo, no autentica actores, no hay `reconnected` para documentos, `changed` y `lost` son alertas, y los hechos derivados no se persisten. PK03 no se ejecuta: termina cuando terminan GO06 y GO07.

AMBIGUEDADES

1. “el hash lo escribe sldb al guardar si el escritor lo omite”. No se define qué hace sldb si el escritor provee un hash distinto del contrato actual del destino: usarlo como hash visto, reemplazarlo o rechazarlo. Obligaría a inventar la política de pinneado ante hash suministrado.
2. “un documento con un campo `__doc_anchors__` queda consultable desde una regla por `anchor_state`”. No queda claro si `anchor_state` se consulta sobre el documento que contiene el ancla o sobre el elemento alcanzado por el camino. Obligaría a inventar dónde vive el campo derivado y cómo se referencia en una regla.

DRY-RUN

Lecturas: DAG y aceptaciones de PK03, GO06 y GO07; GO05 como lenguaje y GO04 como proyección. GO06 leería GO05 y produciría modelo `RuleDoc`, API/CLI de reglas, `Finding`, documentación y CHANGELOG. GO07 leería GO04 y GO05, y produciría atributo `__doc_anchors__`, pinneado en guardado, API de anclas, `provenance_changed`, estados y documentación. No hay arista entre GO06 y GO07: no se transfieren artefactos entre sí; ambos comparten GO05 y GO07 usa además GO04. Validación conjunta: jerarquía de sujetos, findings con severidad y cláusula, `rules explain` con tres exits, anclas `intact/changed/lost`, regla con `anchor_state`, pinneado y alertas en `anchors check`/`stores check`, documentación y CHANGELOG. Nada se ejecuta.

FUTURO

Promoción separada de GO06 y GO07; GO08 consumirá el hash de regla; GO10 retirará shims; deskops consumirá las capacidades en su plan; un humano confirma gates y valida pytest en robocop2.

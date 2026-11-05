## REFORMULACION
PK03 es un agregado del plan `grafo-operable`, repo dueño `sldb`, no ejecutable: termina cuando terminan sus hijos GO06 y GO07. Su propósito es entregar reglas como documentos y anclas documentales con hash de contrato. El resultado sustantivo del paquete es: `RuleDoc` con sujeto por familia de modelo, condición, severidad y momento; `rules check`/`rules explain` con findings, cláusula fallida y exits definidos; ancla `doc:Model:name@sha256:<hash>` con pinneado al guardar, estados `intact/changed/lost` y `anchor_state` consultable desde una regla. Límites: no define modelos de recibo, no autentica actores, no persiste hechos derivados y no modifica deskops; la aceptación conjunta es la del nodo, con el detalle de `anchor_state` verificado en GO07.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Sin ejecutar nada: PK03 no corre; GO06, tras GO05, recibiría el lenguaje, la herencia de modelos y el canal `Finding`, y produciría `RuleDoc`, `rules check/explain` y documentación. GO07, tras GO04 y GO05, recibiría la facet `payload` proyectada y el lenguaje, y produciría anclas `doc:`, pinneado, `anchors check`, `__doc_anchors__`, `anchor_state` y documentación. Entre GO06 y GO07 no hay arista: no se transfieren artefactos; ambos aportan a PK03. La validación conjunta futura usaría un store temporal con modelos `Base/X/Y/Z`, una `RuleDoc` por familia, documentos anclados y una regla con `anchor_state`; comprobaría findings, exits, estados de ancla y docs/CHANGELOG. Dependencias: gates `G_SEMANTICS`, GO04 y GO05; validación con pytest según reglas comunes.

## FUTURO
GO05 y GO04 deben entregar sus contratos antes de ejecutar los hijos. GO08 cableará `stores check` y usará el hash de regla. Un operador humano promueve los TaskDoc y dispone la revisión; deskops/G_CONSUMER consume el resultado en su propio plan.

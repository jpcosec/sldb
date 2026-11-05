REFORMULACION
PK03 es un agregado no ejecutable del plan `grafo-operable`, repo `sldb`. Encarga el paquete “Reglas y anclas”: dotar a sldb de `RuleDoc` evaluable con `rules check`/`rules explain`, y de anclas `doc:` con hash de contrato, estados `intact/changed/lost` y `anchor_state` consultable por reglas. Resultado conjunto: findings con severidad y cláusula fallida; `anchors check` reporta estados; un campo `__doc_anchors__` queda consultable por `anchor_state`. Límites: no define modelos de recibo, no autentica actores, no persiste `anchor_state`; se valida por sus hijos, no por ejecución propia.

AMBIGUEDADES
ninguna.

DRY-RUN
PK03 no se ejecuta: termina cuando terminan GO06 y GO07. GO06 toma el lenguaje de GO05, la herencia de modelos y `Finding` de core; produce `RuleDoc` validada, `rules check`/`explain` y documentación. GO07 toma la facet payload y `field_hashes` de GO04 y el lenguaje de GO05; produce `__doc_anchors__`, pinneado, `anchor_state` derivado y `check_doc_anchors`. No hay arista GO06→GO07: no se transfieren artefactos directamente; ambos aportan al resultado del paquete y pueden avanzar en paralelo tras sus dependencias. Validación conjunta: escenario `Base/X/Y/Z` para familia de regla; `A/B` con edición de contrato para `intact/changed/lost`; `Review/Task` con una regla que usa `anchor_state`; rechazo de valores no `doc:`; alertas de `anchors check`; docs y CHANGELOG. Sin ejecutar.

FUTURO
El operador del desk de sldb promueve los TaskDoc de GO06/GO07 y dispone las revisiones en `reviews/rN.md`; el dueño confirma los gates `G_SEMANTICS`/`G_SEAM`. GO08 cablea `anchors check` en `stores check`; GO10 retira shims; deskops consume después (`G_CONSUMER`).

REFORMULACION  
PK03 es un paquete no ejecutable (`node_role: aggregate`) del plan grafo-operable, repo `sldb`. Propósito: entregar reglas como documentos y anclas a documentos con hash de contrato. Resultado: GO06 define `RuleDoc`, validación al escribir, `rules check` y `rules explain`; GO07 define anclas `doc:Model:name@sha256:<hash>`, pinneado, estados `intact/changed/lost`, `anchors check`, alertas de procedencia y `anchor_state` derivado consultable desde el lenguaje. Límites: no define modelos de recibo, no autentica actores, no persiste hechos derivados y no cambia consumidores. Termina cuando terminan GO06 y GO07.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Hipotético, sin ejecutar. PK03 no se ejecuta: se validan sus hijos. GO06 y GO07 dependen de GO04 y GO05; no hay arista entre hermanos, así que no se transfieren artefactos directamente. GO04 aporta la facet `payload` y staleness; GO05 aporta parser/evaluador y explicación. GO06 consume eso y produce modelo `RuleDoc`, API/CLI de rules, `docs/architecture/rules.md` y CHANGELOG. GO07 consume GO04/GO05 y produce API de anchors, `__doc_anchors__`, pinneado en guardado, `provenance.py`, `anchoring.md` y CHANGELOG. Validación conjunta: store temporal con Base/X/Y/Z; escribir RuleDocs y comprobar sujeto por familia, severidades, `where`, rechazo de reglas mal formadas y exits de `rules explain`; escribir documentos con `__doc_anchors__` y `from:`, editar contrato vs fuera de contrato, borrar destino y comprobar `intact/changed/lost`, alertas y `provenance_changed`; evaluar una regla con `anchor_state`. Como GO07 valida con una regla, la validación conjunta requiere que GO06 esté disponible o que se use el lenguaje de GO05 directamente.

FUTURO  
GO08 cablea `anchors check` en `stores check`; GO10 retira los shims de compatibilidad; deskops consume `RuleDoc` y anclas en su propio plan. Un humano acepta la revisión y promueve los hijos; los gates `G_SEMANTICS` y `G_SEAM` condicionan la ejecución.

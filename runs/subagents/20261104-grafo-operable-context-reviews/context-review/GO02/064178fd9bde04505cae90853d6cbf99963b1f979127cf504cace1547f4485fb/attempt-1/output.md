REFORMULACION
GO02 es un nodo `design`, `delivery`, `owner_repo: sldb`, hijo de PK01. Propósito: fijar semántica, gramática y firma de evaluación del lenguaje de reglas antes de implementarlo. Resultado: `docs/architecture/rules-language.md` con (a)-(f): gramática; caminos, cuantificadores, clausura y sustitución; semántica Datalog estratificada, mundo cerrado e `incomplete`; formato de explicación; hash `__contract__`; firma `eval`; más tabla de equivalencia y ejemplos xfail. Límites: `output_scope: docs/architecture/rules-language.md, tests de spec xfail`; “Sin código salvo los ejemplos como tests de spec marcados xfail”; depende de GO01 y requiere `G_BOUNDARY`; debe producir `G_SEMANTICS` y revisión en frío aceptada.

AMBIGUEDADES
1. Precedencia y asociatividad: “gramática: and/or/not, paréntesis…” no las fija; tampoco “conjunción de nivel superior”. Obliga a inventar cómo parsear `a or b and c` y qué restringe el dominio.
2. Contradicción de operadores: el scope incluye “= != < <= > >=”, pero acceptance exige tabla que cubre “= != >= <=”; omite `>` y `<`. Obliga a decidir si faltan en la tabla o en la aceptación.
3. Sustitución: “con la sintaxis que ya usa where_subject” no se define en el input; obliga a inventar delimitadores/escape o a importar un contrato no suministrado.
4. Error de parseo: “regex inválida = error de parseo” no fija forma ni canal (finding, envelope, excepción); la acceptance pide ejemplo con resultado esperado y obliga a inventarlo.

DRY-RUN
Un ejecutor futuro leería GO02, brief, alcance, decisiones y guía; comprobaría GO01/`G_BOUNDARY`; escribiría el documento y tests xfail; no tocaría código. Validaría cada construcción (a)/(b) con ejemplo, tablas de equivalencia y trivaluada completas, regex inválida y ciclo, `__contract__`/orden/firma, xfail no skipped, y cold review.

FUTURO
GO03 implementa la firma `eval`; GO05 vuelve verdes los xfail; el desk de sldb acepta la revisión y satisface `G_SEMANTICS`; GO01 produce `G_BOUNDARY`. D5-D7 ya están confirmadas y no se reabren.

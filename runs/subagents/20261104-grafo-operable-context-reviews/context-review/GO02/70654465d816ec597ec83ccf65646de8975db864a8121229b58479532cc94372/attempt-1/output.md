## REFORMULACION
GO02 es un nodo `design` del repo `sldb`: producir `docs/architecture/rules-language.md` fijando gramática, caminos, semántica trivaluada/Datalog estratificado, explicación, `__contract__` y la firma `eval`, más ejemplos como tests de spec `xfail`. Su resultado es el documento y `G_SEMANTICS`; depende de GO01 y `G_BOUNDARY`. Límites: no implementa el evaluador ni cambia `where_parse`/`FieldCondition`; solo documenta y deja ejemplos `xfail`, sin código de producción.

## AMBIGUEDADES
1. El input dice “`in [...]`” y, a la vez, “`contains → "x" in f`”. No define si `in` acepta un operando derecho escalar/string —y entonces significa subcadena— o solo listas, ni qué ocurre con tipos incompatibles. Obligaría a inventar la semántica de `in` para strings y el ejemplo de equivalencia de `contains`, que la aceptación exige cubrir.

## DRY-RUN
Un ejecutor futuro leería `brief.md`, `alcance.md`, `decisiones.md` y el nodo GO02; escribiría la especificación en `docs/architecture/rules-language.md`, añadiría los tests de spec `xfail` en `tests/` y no tocaría producción. Dependencias: GO01 y `G_BOUNDARY` como prerrequisitos. Validaría cada construcción con ejemplo y resultado esperado, la tabla de equivalencia, la tabla trivaluada, los caminos, `__contract__` y la firma de `eval`; después pediría revisión en frío para `G_SEMANTICS`. No es agregado: no hay hijos que recorrer.

## FUTURO
GO03 implementará la firma `eval` sobre `GraphBackend`; GO05 hará verdes los `xfail` y unificará el lenguaje; GO10 retirará los shims. El desk de `sldb` acepta la revisión en frío y satisface `G_SEMANTICS`; el TaskDoc fijará rutas y nombres exactos de tests.

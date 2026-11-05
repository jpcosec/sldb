## REFORMULACION
GO02 es un nodo `design` de sldb, no agregado: fija en `docs/architecture/rules-language.md` gramática, caminos, semántica, explicación, hash de contrato y firma `eval`, con ejemplos como tests xfail. Límite: sin código de producción; solo documento y tests de spec xfail. Depende de GO01 y `G_BOUNDARY`; su aceptación incluye revisión en frío y confirmación de D6 por el dueño. Produce `G_SEMANTICS`.

## AMBIGUEDADES
1. “regex ~”: no define sabor, búsqueda o coincidencia completa, ni regex inválida. Obligaría a inventar semántica y ejemplos.
2. “clausura transitiva (+)”: no fija dirección, inclusión del origen, ciclos, duplicados ni propagación de `incomplete`. Obligaría a inventar el resultado esperado.
3. “cuantificadores any/all/none/count” frente a “tabla con not, all, none y count”: omite `any` y no define `incomplete` combinado con `any`; “se propaga como tercer valor solo hacia arriba” no basta para tablas de verdad. Obligaría a inventar esa semántica.
4. “calculado desde field_hashes en orden canónico”: no define el orden ni la serialización. Obligaría a inventar el hash de contrato.
5. “documento enlazado no disponible”: no distingue enlace ausente de store enlazado no presente; afecta `count` y `any`. Obligaría a inventar cuándo es `false` y cuándo `incomplete`.

## DRY-RUN
Lecturas hipotéticas: GO01/G_BOUNDARY, brief, alcance, decisiones, `where_parse`, `FieldCondition`, modelos con `__contract__` y estilo de `docs/architecture/`. Cambios previstos: crear `rules-language.md` y tests de spec xfail; sin tocar código. Dependencias: commit de GO01 que satisface `G_BOUNDARY`. Validaciones futuras: documento existente; tabla completa; ejemplos xfail no skipped; revisión en frío aceptada; D6 confirmado.

## FUTURO
GO01 produce `G_BOUNDARY`; el dueño confirma D6; el desk acepta la revisión en frío; GO03 implementa la firma; GO05 hace verdes los xfail. `G_SEMANTICS` se resuelve con esas acciones, no dentro de GO02.

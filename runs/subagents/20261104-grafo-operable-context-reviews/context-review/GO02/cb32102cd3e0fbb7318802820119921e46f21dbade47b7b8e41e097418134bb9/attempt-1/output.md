## REFORMULACION

GO02 es un nodo de diseño, no agregado y no ejecutable por sí mismo: no modifica código de producción. Repo dueño: sldb. Hijo de PK01, depende de GO01 y requiere G_BOUNDARY. Propósito: fijar la gramática y semántica del lenguaje de reglas antes de implementarlo. Resultado: `docs/architecture/rules-language.md` con gramática (booleanos, comparaciones, `in [...]`, regex, `model <= X`, `has/nonempty`), caminos por relación y campo con `any/all/none/count` y clausura (`+`), sustitución `{campo}`, semántica Datalog estratificado, mundo cerrado por store con “desconocido” a través de links, formato de explicación y definición del hash de contrato; más tabla de equivalencia con `where_parse`/`FieldCondition` y ejemplos como tests xfail. Límite: solo documentación y tests de spec. Aceptación: documento, ejemplos con resultado esperado, tabla completa, xfail hasta GO05, revisión en frío aceptada y confirmación de D6.

## AMBIGUEDADES

1. **Cobertura de operadores.** Cita: “and/or/not, paréntesis, comparaciones, in [...], regex, model <= X, has/nonempty” frente a “la tabla de equivalencia cubre todos los operadores actuales”. Los actuales incluyen `contains`, `starts_with` e `is_null` (alcance.md), que no figuran como construcciones. Obliga a inventar si se añaden producciones o se declaran no equivalentes, recortando o excediendo el alcance.
2. **Declaración del hash de contrato.** Cita: “hash de contrato: definido por el modelo como subconjunto de campos”. Ninguna fuente dice dónde ni con qué sintaxis el modelo declara ese subconjunto; alcance.md solo constata `field_hashes`. Obliga a inventar un campo de modelo o formato nuevo, que `output_scope` (solo doc y tests xfail) no permite materializar.
3. **Propagación de “desconocido”.** Cita: “Datalog estratificado… mundo cerrado por store (a través de links: desconocido, no falso)”. No se define cómo interactúa “desconocido” con `not`, `all/none` y `count`. Obliga a inventar tablas de verdad o semántica trivaluada, potencialmente contradictoria con “Datalog estratificado”.

## DRY-RUN

Lecturas: brief.md, alcance.md, decisiones.md, dag.yaml, commit/pill de GO01 y confirmación de D6. Cambios previstos: escribir `rules-language.md` y tests de spec xfail; sin `src/`. Dependencias: GO01 con G_BOUNDARY satisfecho; GO04/GO05 solo como referencia futura. Validaciones futuras: doc existente, cada construcción con ejemplo, tabla completa, pytest con xfail (no saltados), revisión en frío y D6.

## FUTURO

GO05 convierte los xfail en verdes e implementa parser/evaluador; GO04 aporta la proyección; el dueño confirma D6; el desk de sldb acepta la revisión y resuelve G_SEMANTICS.

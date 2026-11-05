## REFORMULACION

Propósito: retirar de sldb los dos lenguajes de condición viejos cuando la API única ya esté en uso, dejando la documentación alineada. Resultado: `where_parse` y `FieldCondition` inexistentes en `src/` y `docs/`; operadores viejos sin uso sintáctico en docs; goldens conservados como tests del lenguaje nuevo; suite verde; CHANGELOG. Repo: sldb. Límites: `output_scope` (query_engine, graph/language, docs, CHANGELOG); no modifica deskops ni reabre GO05–GO09.

## AMBIGUEDADES

1. "la construcción equivalente de la tabla de GO02": GO02 no está en `depends_on` ni en la cadena declarada (GO10→GO08→{GO06,GO07,GO09}; GO06→GO05). Obliga a localizar o inventar un contrato no declarado.
2. "eq, ne, gt, lt, contains, starts_with, is_null, is_not_null": `alcance.md` enumera solo hasta `is_null` para FieldCondition. `is_not_null` no consta; obliga a decidir si existe o inventarlo.
3. "no devuelve usos como sintaxis de consulta": criterio interpretativo; `contains` y `starts_with` son palabras comunes en prosa. Obliga a inventar qué cuenta como uso sintáctico.
4. "Los goldens de equivalencia se conservan como tests del lenguaje nuevo": no dice dónde viven y `tests/` no está en `output_scope`; obliga a inventar si puede editarlos y cuáles son.
5. "CHANGELOG registra el retiro con la versión": no se fija versión ni política; obliga a inventar el número.

## DRY-RUN

Nodo ejecutable, no agregado. Un ejecutor leería la tabla de GO02, los goldens, la lista de grep y el estado de GO08. Borraría `where_parse`/`FieldCondition` y llamadas residuales, reescribiría cada mención en `docs/`, conservaría los goldens y actualizaría CHANGELOG. Dependencia: GO08 integrado. Validaciones futuras: los dos greps de acceptance, suite completa en el host indicado y revisión del diff de CHANGELOG. Nada ejecutado.

## FUTURO

GO02 produce la tabla de construcciones; GO05/GO08 producen shims y API a retirar; el promotor fija por grep la lista exacta de archivos y la registra en el TaskDoc; un humano corre pytest y escribe la disposición en `reviews/rN.md`.

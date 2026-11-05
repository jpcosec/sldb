## REFORMULACION

GO10 es un nodo de entrega en `sldb` cuyo propósito es retirar los shims `where_parse` y `FieldCondition` dejados por GO05 y reescribir en `docs/` las menciones de sintaxis vieja (`eq, ne, gt, lt, contains, starts_with, is_null, is_not_null`) usando el lenguaje nuevo de GO02. El resultado esperado es: grep limpio en `src/` y `docs/`, goldens conservados como tests del lenguaje nuevo, suite completa verde y CHANGELOG actualizado en la sección vigente. Límites: `output_scope` acotado a `query_engine/`, `graph/language/`, `tests/`, `docs/` y `CHANGELOG.md`; no crea versión nueva. Depende de GO02 y GO08, con GO05/GO06/GO07/GO09 transitivos vía GO08.

## AMBIGUEDADES

1. **Prerrequisito de llamantes no verificado ni dependenciado.** Cita: “Prerrequisito: todos los llamantes del repo usan la API única”. No hay nodo ni criterio de aceptación que lo compruebe, y `output_scope` no cubre llamantes fuera de `query_engine/`. El ejecutor tendría que inventar si migra llamantes externos, los deja rotos o asume que ya están migrados.

2. **Criterio “sintaxis” vs “prosa” no mecanizable.** Cita: “grep -rw de eq, ne, gt, lt, contains, starts_with, is_null, is_not_null en docs/ no devuelve usos como sintaxis de consulta”. Palabras como `contains` o `in` aparecen en prosa y ejemplos; el ejecutor debe decidir caso por caso qué hit es sintaxis, sin regla objetiva.

3. **Alcance de los goldens en `tests/` indefinido.** Cita: “Los goldens viven en tests/, donde GO05 los dejó, y se conservan como tests del lenguaje nuevo”. No se dice si los archivos o identificadores de test pueden conservar `where_parse`/`FieldCondition`; la aceptación no grep-ea `tests/`. El ejecutor tendría que inventar si renombrar símbolos o solo conservar casos.

## DRY-RUN

Un ejecutor futuro leería GO10, la tabla de equivalencias de GO02, los shims de GO05 y la API de GO08. Levantaría el inventario por grep al promover y lo fijaría en el TaskDoc. Borraría `where_parse` y `FieldCondition` de `src/sldb/store/query_engine/` y ajustaría importaciones dentro del `output_scope`; reescribiría ejemplos y bloques de código en `docs/`; conservaría los goldens en `tests/` como tests del lenguaje nuevo; registraría el retiro en la sección vigente de `CHANGELOG.md`. Validaría con grep en `src/` y `docs/`, grep contextual de operadores en `docs/`, suite completa y revisión del CHANGELOG. Depende de GO02 y GO08 ya cerrados; no se ejecuta aquí.

## FUTURO

GO02 fija la tabla de equivalencias que GO10 usa para reescribir. GO08 entrega la API única y la evaluación. El TaskDoc fijará la lista exacta de archivos y tests al promover. La aceptación en frío y la disposición en `reviews/rN.md` las decide quien opera el desk de sldb (D3), no este nodo.

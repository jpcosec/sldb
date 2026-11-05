REFORMULACION
GO10 es un nodo de entrega (`code`) del repo sldb, hijo de PK04. Su propósito es retirar los shims `where_parse` y `FieldCondition` y sustituir en `docs/` las menciones de esos identificadores y de los ocho operadores viejos usados como sintaxis —en bloques cercados o código en línea— por el lenguaje de GO02. Resultado: identificadores ausentes en `src/` y prosa de `docs/` salvo la tabla histórica; operadores ausentes en bloques de `docs/`; goldens conservados como tests del lenguaje nuevo; suite verde y CHANGELOG con la versión vigente. Límites: `output_scope` restringido a `store/query_engine/`, `store/graph/language/`, `tests/`, `docs/` y `CHANGELOG.md`; no toca `effects` ni `findings`; sin ejecución autorizada.

AMBIGUEDADES
1. «grep -r de los identificadores where_parse y FieldCondition en src/ ... no devuelve nada» frente a `output_scope: src/sldb/store/query_engine/, src/sldb/store/graph/language/`. Si queda una referencia en otro directorio de `src/`, GO10 no puede borrarla sin exceder su límite; obliga a inventar si se ignora o se amplía el scope.
2. «toda mención ... reemplazada por el lenguaje nuevo» frente a «con una única excepción nombrada: la tabla de equivalencia histórica». No queda definido si la tabla se conserva íntegra o solo como excepción de grep; obliga a decidir el alcance de la reescritura.
3. «cada mención retirada se reescribe con la construcción equivalente de la tabla de GO02»: esa tabla es operador por operador, no para los nombres `where_parse`/`FieldCondition`; obliga a inventar el texto sustituto de esas menciones en prosa y código.

DRY-RUN
Lecturas: GO02 (`rules-language.md`), salidas de GO05/GO08, shims actuales, Markdown con bloques afectados, goldens y CHANGELOG. Cambios previstos: borrar shims, ajustar imports/llamadas dentro del scope, reescribir bloques de docs, conservar o adaptar goldens, añadir histórico y CHANGELOG. Dependencias: tabla de GO02 y API única de GO05/GO08. Validaciones futuras: greps de aceptación, pytest completo, revisión en frío; sin ejecutar.

FUTURO
GO02 produce la tabla de equivalencias; GO05/GO08 dejan la API y los goldens; el TaskDoc fija archivos, nombres de tests y la lista exacta por grep; un humano o revisor acepta la disposición y promueve el nodo.

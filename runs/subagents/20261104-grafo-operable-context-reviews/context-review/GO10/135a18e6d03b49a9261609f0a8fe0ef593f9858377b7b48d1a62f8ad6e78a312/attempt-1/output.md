REFORMULACION
Propósito: retirar de sldb los shims where_parse y FieldCondition (de GO05) y las menciones en docs/ de ambos y de los operadores eq, ne, gt, lt, contains, starts_with, is_null, is_not_null como sintaxis, sustituyéndolas por el lenguaje nuevo; conservar los goldens de equivalencia como tests del lenguaje nuevo. Repo dueño: sldb. Resultado: grep de where_parse y FieldCondition en src/ y docs/ sin resultados salvo CHANGELOG; suite completa verde; CHANGELOG con versión. Límites: no toca effects (GO09) ni findings (GO08); output_scope query_engine, graph/language, docs/, CHANGELOG.md; prerrequisito GO08 (transitivo GO05, GO06, GO07, GO09). Nodo delivery ejecutable.

AMBIGUEDADES
1. Cita: "en docs/, toda mención de ... los operadores eq, ne, ... como sintaxis" frente a aceptación "grep de where_parse y FieldCondition en src/ y docs/". La aceptación no cubre los operadores; obligaría a inventar si su retirada es bloqueante y qué cuenta como "como sintaxis".
2. Cita: "no devuelve nada salvo CHANGELOG" con grep "en src/ y docs/". CHANGELOG.md está en la raíz, fuera de src/ y docs/; obligaría a inventar si el grep lo incluye o la excepción es inocua.
3. Cita: "reemplazada por el lenguaje nuevo". No fija cómo reescribir cada mención; obligaría a inventar el texto o si basta borrar.

DRY-RUN
Un ejecutor futuro leería GO10, GO08 y los contratos cerrados de GO05-GO07/GO09; haría grep en src/ y docs/; borraría los shims y sus llamadas; reescribiría docs/; conservaría o ajustaría goldens como tests del lenguaje nuevo; actualizaría CHANGELOG; correría pytest completo en el host indicado (robocop2); repetiría grep y verificaría la suite. Dependencia: GO08 cerrado. Validaciones futuras: grep vacío, suite verde, CHANGELOG con versión. Sin ejecutar.

FUTURO
El operador del desk de sldb escribe la disposición en reviews/rN.md; la promoción vía deskops add task fija en el TaskDoc la lista de grep, la versión, el texto de reemplazo y el host de validación; GO08 y sus dependencias deben estar cerradas. La discrepancia de aceptación sobre operadores la resuelve el humano.

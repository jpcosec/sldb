REFORMULACION  
GO02 es un nodo de diseño (`design`, `delivery`) del repo `sldb`: fijar en `docs/architecture/rules-language.md` la gramática, semántica, formato de explicación, hash de contrato y firma de evaluación del lenguaje de reglas, con ejemplos como tests xfail. Límites: sin código de producción salvo esos ejemplos; depende de GO01 y `G_BOUNDARY`; produce `G_SEMANTICS`. No se ejecuta nada.

AMBIGUEDADES  
1. “eval(predicado parseado, sujeto opcional) devuelve una lista de findings con node, holds..., clause, seen”. No se define qué evaluar cuando el sujeto se omite ni qué `node`/`seen` lleva cada finding. Obligaría a inventar si sin sujeto se evalúan todos los documentos, si hay un finding por nodo o uno global, y la forma de `seen`.  
2. “una referencia a un documento inexistente dentro de un store disponible es false”. En un camino multivariado no se aclara si el elemento faltante se omite del conjunto alcanzado o permanece como elemento con predicado falso. Obligaría a inventar el efecto sobre `any/all/none` y `count`.  
3. “__contract__ (lista de nombres; ausente = todos los campos del payload)”. No se define lista vacía ni campos listados ausentes del payload o sin `field_hash`. Obligaría a inventar si vacío significa “ningún campo” o “todos”, y cómo se hashea un campo faltante.

DRY-RUN  
Lecturas previstas: `dag.yaml` (GO02), `brief.md`, `alcance.md`, `decisiones.md`, guía; código existente de `where_parse`, `FieldCondition`, `where_subject` y `field_hashes`. Cambios previstos: crear `docs/architecture/rules-language.md` y tests de spec xfail. Dependencias: GO01 y `G_BOUNDARY` satisfechos; GO03 no es dependencia. Validaciones futuras: pytest con xfail no skipped, ejemplos con resultado esperado, regex inválida y clausura con ciclo, tabla de equivalencia, revisión en frío aceptada y `G_SEMANTICS`.

FUTURO  
GO03 consume la firma de `eval`; GO05 convierte los tests xfail en verdes; el desk de sldb acepta la revisión y satisface `G_SEMANTICS`. La resolución de las ambigüedades corresponde a GO02/TaskDoc, no a esta revisión.

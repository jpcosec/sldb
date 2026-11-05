---
id: task-go02-semantica-gramatica-y-firma-de-evaluacion-del-lenguaje-de-reglas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- docs/architecture/rules-language.md
- tests/test_rules_language_spec.py
- desk/drawer/plans/grafo-operable/dag.yaml
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- commit
- document
---

# GO02: semantica, gramatica y firma de evaluacion del lenguaje de reglas

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO02 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9). Fija la semantica antes de implementar; produce el gate G_SEMANTICS. D6 (Datalog estratificado con incomplete en el borde de links) confirmada por el dueno el 2026-11-04.

## Goal

_Describe the concrete result this task must produce._

Escribir docs/architecture/rules-language.md con los apartados (a)-(f) del contrato y una tabla de equivalencia con where_parse y FieldCondition, mas tests de spec marcados xfail (no skipped) en tests/test_rules_language_spec.py, uno por construccion. Sin codigo de produccion.

## Scope

_State what is in scope and what is out of scope._

Solo docs/architecture/rules-language.md y tests/test_rules_language_spec.py. No se toca src/. Leer antes: src/sldb/store/query_engine/where_parse.py, where_subject.py, where_lookup.py, src/sldb/store/graph/language/field_condition.py, src/sldb/store/graph/facet_match.py, src/sldb/models/relation_type_doc.py (base_models), src/sldb/core/finding.py, docs/cli-envelope.md. El contrato completo del nodo esta en implementation_path. PRECISIONES tras preflight y cold-bundle (2026-11-04, sin tercer intento por tope): (p1) 'model' es el nombre del modelo del documento (su clase sldb); 'familia' de X = X y todos los modelos que lo heredan por base_models; (p2) 'camino' = secuencia de uno o mas pasos (campo, rel:tipo, ^campo, con + opcional en cada paso); en un cuantificador, los dos puntos separan el camino del predicado: any(camino: predicado) es sintaxis, no glosa; (p3) la clausura corta en silencio ante ciclos (el resultado es un conjunto); (p4) seen: para and, las hojas de la primera rama falsa; para or, las de la primera rama verdadera; para not, la hoja negada; para un cuantificador, las hojas del elemento testigo (el primero que falsa un all o cumple un any); (p5) dos model <= en la conjuncion de nivel superior restringen el dominio a la interseccion de las familias; (p6) __contract__ ausente (atributo no definido) = todos los campos del payload del documento sujeto; __contract__ = [] (definido y vacio) = error al cargar el modelo; (p7) documento inexistente = el store resuelve la referencia a nada; store enlazado no disponible = la referencia apunta a un store que no se puede abrir; (p8) la tabla cubre los 19 operadores enumerados (seis comparadores por separado); (p9) N xfailed = una por construccion documentada, se fija en el propio test y debe ser >= 25; (p10) la revision en frio la acepta quien opera el desk de sldb escribiendo la disposicion en desk/drawer/plans/grafo-operable/reviews/.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO02 scope): Documento docs/architecture/rules-language.md que fija: (a) gramática: and/or/not con precedencia not > and > or, asociativos a la izquierda, paréntesis para agrupar (la "conjunción de nivel superior" es la cadena de and que queda arriba tras parsear con esa precedencia), comparaciones = != < <= > >=, in ("x" in f: pertenencia si f es lista, subcadena si f es string, false para otros tipos; f in [...]: pertenencia de un escalar en una lista literal), regex ~ (sabor Python re, semántica de búsqueda como el ~ actual de where_parse, regex inválida = error de parseo: la excepción WherePredicateError existente, que la CLI convierte en Finding error en el envelope), model <= X, has/nonempty, y las construcciones equivalentes a los operadores actuales contains, starts_with, is_null, is_not_null (como operadores propios o como derivadas documentadas); (b) caminos: un paso se escribe como nombre de campo (depends_on: sigue las aristas references que ese campo declara; un nombre que el modelo del documento actual no declara como referencia produce el conjunto vacío, no un error), rel:<tipo> (sigue las aristas de ese tipo de relación, p. ej. rel:task_activates) o con prefijo ^ para la inversa (^subject: los documentos cuyo campo subject apunta al actual); cuantificadores any/all/none sobre los elementos alcanzados, con un predicado entre paréntesis; count(camino: predicado) es un entero que solo se usa dentro de una comparación (count(depends_on: status = "open") = 0); clausura transitiva: el signo + pegado al paso (depends_on+, rel:tipo+, ^subject+) sigue ese paso repetidamente en la misma dirección, origen excluido, resultado como conjunto sin duplicados, termina ante ciclos; sustitución {campo} desde el payload del sujeto, con la sintaxis que ya usa where_subject: el nombre del campo entre llaves, sin escapes, reconocido solo fuera de literales entre comillas, y un campo ausente o no escalar hace que el predicado no se cumpla; (c) semántica: bivaluada dentro del store (mundo cerrado por store, Datalog estratificado, negación solo estratificada, sin funciones salvo comparaciones); una referencia a un documento inexistente dentro de un store disponible no produce elemento: se omite del conjunto alcanzado por el camino (ver (f)); una referencia que cae en un store enlazado no disponible (no resoluble al evaluar) da incomplete; incomplete se combina con lógica trivaluada de Kleene fuerte para and/or/not, any = or sobre los elementos, all = and, none = not any, una comparación con count es incomplete si algún elemento del camino es incomplete; cualquier comparación u operador con un operando incomplete es incomplete (Kleene), y un predicado evaluado sobre un elemento incomplete es incomplete; una regla error con resultado incomplete falla con explicación "incomplete", una alert lo reporta; (d) formato de explicación: cláusula fallida, nodo, valor visto, en el envelope; (e) hash de contrato: el modelo declara el subconjunto de campos con el atributo de clase __contract__ (lista de nombres; ausente = todos los campos del payload); se calcula como sha256 de las líneas "<campo>=<field_hash>" ordenadas por los bytes UTF-8 del nombre del campo, unidas por \n, sin salto final, codificadas en UTF-8; (f) la firma de evaluación que GO03 implementa: eval(predicado parseado, sujeto opcional) devuelve una lista de findings con node, holds (true/false/incomplete), clause, seen; con sujeto, un finding para ese sujeto; sin sujeto, un finding por cada documento del dominio: todos los documentos del store, salvo que el predicado sea una conjunción de nivel superior que contenga model <= X, en cuyo caso el dominio son los documentos de esa familia (un model <= X anidado bajo not, or, un cuantificador o un camino no restringe el dominio); seen = mapa campo → valor leído para las hojas de la cláusula que decidió el resultado; una hoja incomplete aporta el valor {"incomplete": "<referencia no resuelta>"}. Una referencia a un documento inexistente se omite del conjunto alcanzado por un camino (all sobre conjunto vacío = true, any = false, count = 0). __contract__ vacío = error al cargar el modelo; un campo listado ausente del payload aporta la línea "<campo>=" con hash vacío. Tabla de equivalencia con where_parse y FieldCondition, operador por operador; las construcciones equivalentes del lenguaje nuevo no usan los nombres eq, ne, gt, lt, contains, starts_with, is_null, is_not_null como operadores (p. ej. contains → "x" in f, starts_with → f ~ "^x", is_null → not has(f)). Sin código salvo los ejemplos como tests de spec marcados xfail. ACEPTACION: El documento existe y cada construcción de (a) y (b) tiene un ejemplo con resultado esperado, incluidos regex inválida y clausura con ciclo; la tabla cubre has, nonempty, in, ~, model <=, = != < <= > >=, eq, ne, gt, lt, contains, starts_with, is_null, is_not_null; el ejemplo de regex inválida espera WherePredicateError; la tabla trivaluada cubre and, or, not, any, all, none y la comparación con count; la sintaxis de caminos (campo, rel:tipo, ^) tiene un ejemplo cada una; __contract__, su orden canónico y la firma de eval están definidos; los ejemplos están como tests xfail (no skipped) hasta GO05; revisión en frío aceptada. Produce G_SEMANTICS. REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 3: toda capacidad nueva entra documentada en docs/architecture; regla 6: ante un contrato ausente registrar la hipotesis en este TaskDoc, no inventar API).

## Validation

_List the checks required before this task can close._

- pytest tests/test_rules_language_spec.py -q muestra N xfailed y 0 skipped
- grep -c "^## " docs/architecture/rules-language.md >= 7 (gramatica, caminos, semantica, explicacion, hash de contrato, firma eval, tabla de equivalencia)
- revision en frio del documento aceptada por quien opera el desk de sldb (reviews/ del plan)

## Done When

_Name the observable condition that makes the task complete._

rules-language.md existe con las secciones (a)-(f), cada construccion tiene ejemplo con resultado esperado, la tabla cubre los 18 operadores listados en la aceptacion, los xfail corren sin skipped, y G_SEMANTICS queda satisfied en dag.yaml citando el commit.

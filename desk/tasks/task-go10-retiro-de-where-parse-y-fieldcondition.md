---
id: task-go10-retiro-de-where-parse-y-fieldcondition
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
- src/sldb/store/query_engine/where_parse.py
- src/sldb/store/query_engine/__init__.py
- src/sldb/store/graph/language/field_condition.py
- src/sldb/store/graph/language/field_condition_translation.py
- src/sldb/store/graph/language/facet_filter.py
- src/sldb/store/graph/language/__init__.py
- src/sldb/store/graph/language/predicate_cursor.py
- src/sldb/store/graph/language/predicate_tokens.py
- src/sldb/store/graph/payload_match.py
- src/sldb/store/graph/facet_match.py
- src/sldb/store/graph/__init__.py
- src/sldb/core/exceptions/where_predicate_error.py
- src/sldb/core/exceptions/__init__.py
- src/sldb/core/finding.py
- src/sldb/cli/commands/graph.py
- src/sldb/api/__init__.py
- src/sldb/api/graph/__init__.py
- src/sldb/api/notations/__init__.py
- src/sldb/notations/where_check.py
- contracts/layers.toml
- contracts/queries/sldb/sections_for_taskdoc_document.json
- contracts/queries/sldb/semantic_neighborhood_integration_kgdb.json
- contracts/queries/sldb/documents_tagged_domain_contract.json
- contracts/queries/sldb/documents_near_domain_workflow_task_tag.json
- contracts/queries/sldb/documents_near_taskdoc_model.json
- docs/architecture/graph-backend.md
- docs/architecture/rules-language.md
- docs/architecture/superseded-code-audit.md
- docs/architecture/code-docstring-indexing-handoff.md
- docs/architecture/code-docstring-indexing.spec.md
- docs/architecture/notations-and-views.md
- docs/requests/sldb-knowledge-graph-integration.md
- docs/user-manual.md
- CHANGELOG.md
- tests/store/test_predicate_language.py
- tests/store/test_where_retired.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO10: Retiro de where_parse y FieldCondition

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO10 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK04; regla 4 de alcance.md: el retiro de los lenguajes viejos es un nodo explicito. GO05 (8be66bde) dejo where_parse/compile_where y FieldCondition como shims deprecados detras de la API unica; GO06-GO09 ya usan solo el lenguaje nuevo. GO10 los borra de src/ y de docs/.

## Goal

_Describe the concrete result this task must produce._

Sin los identificadores where_parse ni FieldCondition en src/ ni en docs/ (salvo la tabla historica de rules-language.md bajo 'Historico'); sin los ocho operadores viejos en bloques de codigo de docs/ fuera de esa tabla; cada mencion reescrita con la construccion equivalente; goldens conservados como tests del lenguaje nuevo; CHANGELOG en la seccion en curso.

## Scope

_State what is in scope and what is out of scope._

En alcance: borrar where_parse.py (y compile_where), field_condition.py, field_condition_translation.py y el codigo muerto de facet_match (drawer task-tras-go05-quedan-sin-uso-las-funciones-de-facet-match-y-el-retiro-de-los-shims); los importadores residuales de src/; los JSON de contracts/queries/sldb que usan FieldCondition; los Markdown de docs/ listados en files (obtenidos por grep al promover); CHANGELOG.md; tests. Fuera: cambios de semantica del lenguaje; el resto de deudas del drawer.

PRINCIPIO DEL DUENO (2026-11-05): invariantes de un documento como validadores pydantic; los tests solo prueban rechazo. Aplicado aqui: (q1) el formato nuevo de FacetFilter se valida con pydantic: un StructuredQuery con la clave vieja conditions es rechazado con ValidationError que nombra el campo (un test de rechazo); no se agregan tests que reafirmen lo que ya prueban los existentes.

PRECISIONES AL PROMOVER (2026-11-07):
r1 (WherePredicateError): sale de where_parse.py a src/sldb/core/exceptions/where_predicate_error.py (capa 0; misma clase: ValueError y SLDBError, mismo mensaje) y se reexporta desde sldb.core.exceptions, sldb.store.graph.language y sldb.api; la importacion publica es from sldb.api import WherePredicateError. Sin alias ni modulo puente where_parse (decision del coordinador de proyecto, 2026-11-07). Consumidor externo afectado: pron importa sldb.store.query_engine.where_parse.WherePredicateError (pron/src/pron/world/storage/structural_query.py, pron/src/pron/sexpr/resolving/pending_match.py, pron/tests/test_layer_contract.py); el coordinador le avisa por inbox al integrar; GO10 no toca pron. Si con esto la arista models->store de R6 desaparece (RuleDoc ya no importa nada de store), se quita la entrada upward y el pending R6 de contracts/layers.toml; si no, quedan.
r2 (graph query): FacetFilter pierde conditions (list[FieldCondition]) y gana where: str, un predicado del lenguaje evaluado sobre la facet como hoy lo hace payload_match/facet_match con la traduccion de GO05; los cinco JSON de contracts/queries/sldb se reescriben con la columna nueva de la tabla de rules-language.md seccion 7 y tests/store/test_example_queries.py debe seguir devolviendo los mismos ids (si no, es un bug del reemplazo). sldb graph query deja de emitir el warning deprecated/field-condition; core/finding.py deja de nombrar FieldCondition. El CHANGELOG lo registra como cambio de contrato: el JSON de sldb graph query ya no acepta conditions; usa where con un predicado del lenguaje.
r3 (docs, grep mecanico): el grep de operadores se hace como lo fija la aceptacion (palabras completas dentro de bloques cercados y de codigo en linea de los .md de docs/). Toda aparicion en esos bloques se reescribe con la construccion equivalente de la tabla; si una aparicion no es un operador de FieldCondition (otra API, una palabra de un ejemplo ajeno), se reescribe el ejemplo para no usar la palabra sin cambiar su significado, y se reporta cada caso. La tabla historica se mueve bajo un encabezado que contenga la palabra Historico y queda integra.
r4 (goldens): tests/fixtures/where_goldens y los tests de equivalencia de tests/store/test_predicate_language.py se conservan como tests del lenguaje nuevo: la columna vieja queda como dato del golden (texto), sin importar los shims. tests/store/test_where_retired.py (nuevo) hace el grep de la aceptacion sobre src/ y docs/ y falla si aparece algo.
r5 (tests existentes): los tests que hoy ejercitan los shims (DeprecationWarning, compile_where, FieldCondition, warning de graph query) se borran o se reescriben al lenguaje nuevo; es la unica excepcion a 'tests existentes sin cambios' y se reporta archivo por archivo.

PRECISIONES (preflight de GO10, 2026-11-07):
r6 (codigo muerto): en src/sldb/store/graph/facet_match.py se borran matches_filters, facet_matches, condition_matches y las funciones ordered_* (las que nombra el drawer task); ademas, cualquier funcion o modulo de src/ que quede sin importador en src/ ni en tests/ tras retirar los shims (comprobado por grep) se borra y se reporta.
r7 (lista de docs): los Markdown de docs/ en files son la lista obtenida por grep al promover y es la de partida; si el grep de la aceptacion encuentra otro archivo, se agrega al trabajo y se reporta (no es desvio).
r8 (formato de goldens): no cambia: tests/fixtures/where_goldens/where_parse.json y field_condition.json siguen siendo listas de {old, matches} (old como string en where_parse.json y como dict {field, op, value} en field_condition.json; GO05 p13). Los nombres de archivo de fixtures y tests son libres (la aceptacion no hace grep en tests/). Los tests leen old como dato, sin importar ningun shim.
r9 (casos ajenos en docs): si la palabra aparece en un ejemplo que es un filtro, se reescribe con la construccion equivalente de la tabla; si aparece en codigo ajeno (otra API, un metodo de Python, un nombre de campo), se cambia lo minimo en el bloque para no usar esa palabra conservando lo que el ejemplo muestra (renombrar un campo de ejemplo, usar la expresion equivalente de Python). Cada caso se lista en el reporte; el coordinador los revisa al integrar.
r10 (R6): RuleDoc (src/sldb/models/rule_doc.py) importa de forma diferida el parser de store/graph/language; GO10 no mueve el parser, asi que la arista models->store sigue y las entradas [allow].upward [models, store] y [[pending]] R6 de contracts/layers.toml quedan como estan (su reparacion es el drawer task-r6-...). Mover solo WherePredicateError a core no la cierra.

PRECISIONES (cold-bundle de GO10, 2026-11-07):
r11 (esquema de FacetFilter): facet: str sigue igual y obligatorio; where: str = "" (vacio = sin condicion, el filtro se cumple como hoy un conditions vacio); model_config extra="forbid" en FacetFilter, de modo que un JSON con conditions es rechazado con ValidationError que nombra conditions (r13 queda cubierto por esto; StructuredQuery no cambia su model_config).
r12 (forma del JSON): en cada archivo de contracts/queries/sldb, cada {"facet": X, "conditions": [c1, c2, ...]} pasa a {"facet": X, "where": "<e1> and <e2> and ..."}, donde ei es la construccion de la columna nueva de la tabla de rules-language.md seccion 7 para ci (las conditions eran conjuntivas); una lista vacia pasa a where "". Nada mas del JSON cambia.
r13 (rechazo): cubierto por extra="forbid" de r11.
r14 (campos de un where sobre payload): los campos que nombra un where son las hojas de campo del predicado parseado (las mismas que alimentan seen); unprojected_fields las usa en lugar de c.field. Un where de facet admite el subconjunto sin caminos (como el eval de GO03): un camino (rel:, ^, paso con punto que no sea ruta de campo de H9) es SLDBGraphArgumentError que lo nombra.
r15 (base de WherePredicateError): hereda de ValueError y de sldb.core.exceptions.SLDBError; sldb.store.exceptions.SLDBError es la misma clase reexportada (store/exceptions.py importa de core), asi que no hay dos clases.
r16 (docs listados sin coincidencias): un archivo de la lista que tras el trabajo ya no tiene coincidencias del grep no se toca mas; si nunca las tuvo, no se modifica y se reporta.
r17 (version del CHANGELOG): la seccion en curso es la cabecera "## 0.1.13 — not released yet" de CHANGELOG.md; la entrada de GO10 va en ella, con el cambio de contrato de sldb graph query (r2) y el traslado de WherePredicateError a sldb.api (r1).
r18 (test_predicate_language): _old_where y _old_field_condition se eliminan; los tests de equivalencia leen old del golden como dato (string o dict) y evaluan la columna nueva (la expresion equivalente de la fila, ya presente en el test como construction) con el lenguaje nuevo, comparando con matches y con las diferencias ya fijadas (WHERE_DIFFERENCES, FIELD_CONDITION_DIFFERENCES); ninguna fila se elimina. _capture se elimina (ya no hay codigo viejo con que capturar).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO10 scope): Borrar los shims de GO05 (where_parse y FieldCondition) y cualquier importador residual en src/ que el grep delate (el output_scope cubre todo src/ para eso), y, en docs/, toda mención de where_parse, FieldCondition y de los operadores eq, ne, gt, lt, contains, starts_with, is_null, is_not_null como sintaxis, es decir dentro de bloques de código cercados (```) o de código en línea (`...`) de los Markdown de docs/; la prosa queda excluida por construcción (el grep se restringe a esos bloques; lista obtenida al promover), reemplazada por el lenguaje nuevo: las menciones de los identificadores where_parse y FieldCondition se sustituyen por el nombre de la API única (where_matches y la gramática de rules-language.md) y las de operadores por la construcción equivalente de la tabla; la tabla histórica de rules-language.md se conserva íntegra bajo su encabezado. Los goldens viven en tests/, donde GO05 los dejó, y se conservan como tests del lenguaje nuevo; los nombres de archivos e identificadores de tests son libres (la aceptación no hace grep en tests/). La versión del CHANGELOG es la cabecera vigente del CHANGELOG (la sección en curso), no un número nuevo. Prerrequisito: todos los llamantes del repo usan la API única, lo que GO05 garantiza por su scope (enruta where_matches, edges_holding, StructuredQuery y --where) y GO10 comprueba mecánicamente con su grep; GO05, GO06, GO07 y GO09 son prerrequisitos transitivos vía GO08 (GO08 depende de GO06, GO07 y GO09; GO06 de GO05). Regla 4 de alcance.md: el retiro es un nodo explícito, este. Los goldens de equivalencia se conservan como tests del lenguaje nuevo. ACEPTACION: grep -r de los identificadores where_parse y FieldCondition en src/ y en todo docs/ (prosa incluida: son nombres de código, no palabras) no devuelve nada, con una única excepción nombrada: la tabla de equivalencia histórica de docs/architecture/rules-language.md, que se conserva bajo un encabezado "Histórico"; grep -rw de los ocho operadores restringido a bloques de código cercados y código en línea de los Markdown de docs/ no devuelve nada fuera de esa misma tabla (las equivalencias de GO02 no reutilizan esos nombres, así que el reemplazo no vuelve a dispararlo; la lista exacta de archivos se fija por grep al promover y queda en el TaskDoc); cada mención retirada se reescribe con la construcción equivalente de la tabla de GO02; la suite completa verde; CHANGELOG registra el retiro con la versión. OUTPUT_SCOPE: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/ (solo importadores residuales que el grep delate), tests/, docs/, CHANGELOG.md REGLAS COMUNES: alcance.md (regla 2: no cierra con tests rojos ni saltados; regla 4: retiro en nodo explicito, este; regla 6: hipotesis en el TaskDoc).

## Validation

_List the checks required before this task can close._

- grep -rn 'where_parse\|FieldCondition' src/ docs/ sin resultados fuera de la tabla historica de rules-language.md (bajo Historico)
- grep -rw de eq, ne, gt, lt, contains, starts_with, is_null, is_not_null en bloques de codigo de docs/*.md sin resultados fuera de esa tabla (tests/store/test_where_retired.py)
- StructuredQuery con conditions rechazado con ValidationError (test de rechazo); tests/store/test_example_queries.py devuelve los mismos ids con los JSON reescritos
- goldens de equivalencia verdes como tests del lenguaje nuevo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa verde (una vez, al final del nodo, la corre el supervisor)
- CHANGELOG registra el retiro en la seccion en curso

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO10 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

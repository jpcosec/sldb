---
id: task-go05-lenguaje-de-predicados-unificado
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
- src/sldb/store/graph/language/__init__.py
- src/sldb/store/graph/language/field_condition.py
- src/sldb/store/graph/language/predicate_ast.py
- src/sldb/store/graph/language/predicate_parser.py
- src/sldb/store/graph/language/predicate_eval.py
- src/sldb/store/graph/language/predicate_paths.py
- src/sldb/store/graph/language/predicate_explain.py
- src/sldb/store/graph/backend/parser.py
- src/sldb/store/graph/backend/tokens.py
- src/sldb/store/graph/backend/evaluate.py
- src/sldb/store/graph/backend/eval.py
- src/sldb/store/graph/backend/networkx_backend.py
- src/sldb/store/graph/executor.py
- src/sldb/store/graph/payload_match.py
- src/sldb/store/query_engine/where_parse.py
- src/sldb/store/query_engine/where_subject.py
- src/sldb/store/query_engine/structural_queries.py
- src/sldb/api/where.py
- src/sldb/api/edges/edges_holding.py
- src/sldb/cli/parsers/find.py
- src/sldb/cli/commands/find.py
- src/sldb/cli/commands/find_filter.py
- src/sldb/cli/commands/graph.py
- docs/architecture/rules-language.md
- docs/architecture/graph-backend.md
- CHANGELOG.md
- tests/test_rules_language_spec.py
- tests/store/test_predicate_language.py
- tests/fixtures/where_goldens/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO05: Lenguaje de predicados unificado

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO05 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK02. Hoy hay dos lenguajes de condicion (where_parse y FieldCondition), ninguno cruza relaciones ni tiene or/not/parentesis, y --where re-extrae el payload. GO02 fijo la semantica (docs/architecture/rules-language.md, 52 xfail), GO03 la costura GraphBackend (eval sobre el subconjunto sin caminos) y GO04 la facet payload en el indice (d7eefdeb). GO05 implementa el lenguaje completo sobre esas dos piezas y deja los lenguajes viejos como shims deprecados.

## Goal

_Describe the concrete result this task must produce._

Un parser y un evaluador del lenguaje de GO02 (booleanos completos, caminos con cuantificadores, clausura transitiva, sustitucion desde el sujeto, incomplete en el borde de links, explicacion estructurada) detras de GraphBackend.eval y de una API unica que usan where_matches, edges_holding, StructuredQuery y --where; where_parse y FieldCondition quedan como shims con DeprecationWarning; los 52 tests xfail de GO02 pasan a verdes.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/graph/language/ (AST, parser, evaluador, caminos, explicacion; FieldCondition como shim), src/sldb/store/graph/backend/ (eval deja de levantar NotImplementedError ante caminos), src/sldb/store/query_engine/ (where_parse y compile_where como shims), src/sldb/api/where.py y src/sldb/api/edges/edges_holding.py (enrutados a la API unica), la CLI --where de docs find y su --explain, el envelope de sldb graph query, docs/architecture/rules-language.md y graph-backend.md, CHANGELOG.md, tests. Fuera: RuleDoc y rules check (GO06), anclas doc: y la produccion de F__anchor_state (GO07), transiciones como datos (GO09), evaluacion incremental (GO08), retiro de los shims (GO10), la firma de __indexed__ en contract_signature (drawer task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload).

HEREDADO DE NODOS ANTERIORES: (h1, de GO03 H4) GraphBackend.eval sin sujeto evalua sobre todos los documentos de la proyeccion cargada (rules-language.md, dominio sin sujeto); hoy devuelve [] con proyeccion None. (h2, de GO03 H1) eval recibe el predicado como texto y lo parsea; GO05 expone ademas el tipo predicado parseado publico que eval acepta. (h3, de GO04 H2/H3/H6) la facet payload solo existe en nodos de documento; un campo nulo no llega a la proyeccion; un campo que ningun modelo proyecta es SLDBGraphArgumentError. (h4) El comando de la CLI que entra por la via vieja es sldb graph query (recibe un StructuredQuery con FieldCondition como dicts JSON); --where es el de sldb docs find.

PRECISIONES (preflight de GO05, 2026-11-06):
p1 (comando viejo): el comando de consulta estructurada que entra por la via vieja es sldb graph query (src/sldb/cli/parsers/graph.py, "Run a structured query from a JSON file"). Cuando su StructuredQuery trae FieldCondition como dicts, el envelope (sldb --envelope graph query <archivo>) lleva en warnings una entrada con la forma de docs/cli-envelope.md: level "warning", code "deprecated/field-condition", subject "graph query", what que nombra el reemplazo (la expresion del lenguaje nuevo). La salida de data no cambia.
p2 (gramatica): la sintaxis de booleanos, caminos (campo, rel:tipo, ^campo), cuantificadores any/all/none/count, clausura, precedencia, sustitucion {campo} e incomplete es la de docs/architecture/rules-language.md secciones 1-3 y 6 (G_SEMANTICS satisfecho); los 52 tests de tests/test_rules_language_spec.py son la spec ejecutable y no se modifican salvo quitar la marca xfail. Nada de sintaxis se inventa fuera de ese documento; un hueco se registra como hipotesis.
p3 (--explain): sldb docs find --where <expr> --explain agrega a data la clave findings: lista con un finding (node, holds, clause, seen; rules-language.md seccion 4) por cada documento evaluado, incluidos los que no cumplen; el resultado de find (los documentos que cumplen) no cambia. Sin --explain la salida es identica a la actual. La clave de rules explain sigue siendo de GO06 (H10).
p4 (anchor_state): GO07 aun no produce F__anchor_state; el alias se prueba con una proyeccion sintetica cargada en el backend (load(indice, proyeccion)) cuya facet de origen trae la entrada F__anchor_state, y con otra sin ella (has(anchor_state) es false). No se escribe nada de GO07.
p5 (goldens): antes de tocar src/, un primer commit captura con el codigo de main tests/fixtures/where_goldens/where_parse.json y tests/fixtures/where_goldens/field_condition.json: para cada fila de la tabla de equivalencia (rules-language.md seccion 7), la expresion vieja y la lista ordenada de nombres de los payloads que cumple, sobre un conjunto fijo de payloads definido en tests/store/test_predicate_language.py (cubre null, listas, campo ausente, numeros, strings). El test de equivalencia evalua la columna nueva sobre los mismos payloads y compara con el golden; los goldens no se regeneran despues.
p6 (extract): Validator.extract es sldb.runtime.validation.Validator.extract; el test lo cuenta con monkeypatch (como test_status_closed_is_answered_with_zero_extractions de GO04).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO05 scope): Parser y evaluador del lenguaje de GO02 sobre el backend de GO03 y la facet payload de GO04: booleanos completos, caminos con cuantificadores, clausura transitiva, sustitución desde el sujeto, incomplete en el borde de links, explicación estructurada. Alias genérico al atravesar un campo: cuando un camino atraviesa un campo F del documento origen y la facet del origen tiene una entrada derivada F__anchor_state (GO07 la produce), cada elemento alcanzado expone esa entrada bajo el nombre anchor_state; si la entrada no existe, anchor_state no está definido (has(anchor_state) es false). Compatibilidad: antes de cambiar nada, se capturan goldens del resultado de cada expresión de la tabla de GO02 con where_parse y FieldCondition actuales; luego la gramática nueva (superconjunto) reemplaza a where_parse, que queda como shim que delega en el parser nuevo y emite warnings.warn(DeprecationWarning); FieldCondition queda como shim que traduce al AST nuevo con el mismo aviso; en la CLI, --where entra siempre por la vía nueva y nunca avisa; el único comando de la CLI que entra por la vía vieja es el de consulta estructurada, el que hoy recibe FieldCondition como dicts JSON (nombre exacto del comando fijado en el TaskDoc), y ese agrega una entrada a la lista warnings del envelope (docs/cli-envelope.md); en Python, llamar a where_parse/compile_where o construir FieldCondition emite DeprecationWarning; los operadores de where_parse no avisan por sí mismos, porque la gramática nueva los incluye idénticos. Los tests de equivalencia comparan el resultado nuevo con los goldens. Los tests xfail de GO02 pasan a verdes. API única detrás de where_matches, edges_holding, StructuredQuery y --where. El retiro de los shims es GO10. ACEPTACION: Tests de spec de GO02 verdes; tests de equivalencia contra goldens verdes; sldb docs find --where con any()/all() sobre una relación responde desde la CLI con envelope y, con --explain, la cláusula fallida por documento; un test cuenta cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos de un modelo de este repo; un test captura el DeprecationWarning al llamar a where_parse y al construir un FieldCondition, otro captura la entrada en warnings del envelope de graph query con filtros dict, y otro comprueba que --where con la misma expresión no avisa; CHANGELOG y docs/architecture actualizados. OUTPUT_SCOPE: src/sldb/store/query_engine/, src/sldb/store/graph/language/, src/sldb/api/where.py, src/sldb/api/edges/edges_holding.py (enrutado a la API única), CLI --where, docs/architecture/, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: toda capacidad nueva entra con spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 4: --where actual sigue funcionando; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis en este TaskDoc, no inventar API). Semantica: docs/architecture/rules-language.md (GO02). Costura: docs/architecture/graph-backend.md (GO03, GO04).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/test_rules_language_spec.py sin xfail ni skipped (los 52 pasan a verdes, sin marca xfail)
- tests de equivalencia contra los goldens de where_parse y FieldCondition capturados antes de tocar codigo
- test que cuenta cero llamadas a Validator.extract al evaluar un --where sobre todos los documentos de un modelo de este repo
- tests de DeprecationWarning (where_parse, compile_where, FieldCondition), de warnings en el envelope de sldb graph query con filtros dict, y de --where sin aviso
- sldb docs find --where con any()/all() sobre una relacion y --explain probado por CLI con envelope
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO05 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

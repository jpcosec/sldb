---
id: task-go06-ruledoc-rules-check-y-rules-explain
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- pytest tests/api/test_rules.py
- tests/api/test_rules.py
- 622da0b5b2abb2ad2b090f382b85ae12714eaffd
- desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md
- desk/drawer/tasks/task-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store.md
depends_on: []
pills: []
files:
- src/sldb/models/rule_doc.py
- src/sldb/models/__init__.py
- src/sldb/api/rules/__init__.py
- src/sldb/api/rules/rules_check.py
- src/sldb/api/rules/rules_explain.py
- src/sldb/api/rules/rule_subjects.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/rules.py
- src/sldb/cli/parsers/rules.py
- src/sldb/cli/parsers/__init__.py
- src/sldb/cli/dispatcher.py
- contracts/layers.toml
- docs/architecture/rules.md
- docs/opsys/bridge_primitives/README.md
- CHANGELOG.md
- tests/api/test_rules.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO06: RuleDoc, rules check y rules explain

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO06 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK03. sldb evalua reglas declaradas y los consumidores las autoran como documentos (G_BOUNDARY, atom-sldb-evaluates-declared-rules-consumers-author-them). GO05 (8be66bde) dejo el lenguaje de predicados y GraphBackend.eval completos; GO06 agrega el documento RuleDoc y los comandos que lo evaluan.

## Goal

_Describe the concrete result this task must produce._

Modelo RuleDoc (subject como expresion model <= X, where opcional, condition, severidad error|alert, momento on_write|on_transition|on_check, message opcional) validado al escribir; sldb rules check [--subject DOC] emite Finding de core con exit 1 solo ante error; sldb rules explain RULE SUBJECT devuelve el finding de eval con exits 0/1/2/3; docs/architecture/rules.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: el modelo RuleDoc, api/rules (check, explain, resolucion de sujetos y reglas), el comando sldb rules (check, explain) con su parser y su registro en el dispatcher, docs/architecture/rules.md, la marca de reemplazo en docs/opsys/bridge_primitives/README.md, CHANGELOG.md, tests. Fuera: evaluacion incremental y cableado on_write/on_transition (GO08), anclas doc: (GO07), transiciones como datos (GO09), retiro de shims (GO10).

PRINCIPIO DEL DUENO (2026-11-05): las invariantes de UN documento van como validadores pydantic del modelo; las invariantes entre documentos, como RuleDoc. Los tests solo prueban rechazo. Aplicado aqui: (q1) que condition y where parseen, que subject sea una expresion del lenguaje de la forma model <= X (o conjuncion que la contenga), y el vocabulario de severidad y momento (Literal) son validadores pydantic de RuleDoc (field_validator / Literal), de modo que construir o escribir una RuleDoc mal formada levanta el ValidationError del modelo con el campo y el motivo, por la via de escritura existente (sldb docs create/edit y la API). Que X resuelva a un modelo registrado depende del store, no del documento: se comprueba en la escritura (api) con el error existente de sldb para modelo desconocido, y no como validador del modelo. (q2) Los tests de RuleDoc mal formada prueban rechazo: un test por campo (condition, where, severidad, momento, sujeto) que espera el error; no hay tests que reafirmen que una RuleDoc valida se acepta mas alla de los que la aceptacion pide para check y explain.

HEREDADO: (h1) la familia de model <= X sale de base_models (GO05 p9, 8d7bee13). (h2) El finding de eval es el de rules-language.md seccion 4 (node, holds, clause, seen); la clave del envelope para rules explain la fija este nodo (H10 de rules-language). (h3) GO05 H6: los cambios de resultado del lenguaje nuevo frente a where_parse/FieldCondition ya estan en main; las reglas usan solo el lenguaje nuevo.

PRECISIONES (preflight de GO06, 2026-11-06):
p1 (envelope de rules explain): data = {"rule": "RuleDoc:<nombre>", "subject": "<Model:name>", "finding": {"node", "holds", "clause", "seen"}}, con el finding exactamente como lo devuelve GraphBackend.eval / eval_predicate (rules-language.md seccion 4; holds como "true", "false" o "incomplete"). La clave finding cierra H10 de rules-language.md para rules explain; el doc lo dice.
p2 (Finding.what): explicacion = "<clause> (seen: <seen en JSON compacto, claves ordenadas, ensure_ascii=False>)". Con message: what = message + " | " + explicacion. Sin message: what = explicacion.
p3 (exit 3): data = {"rule": "RuleDoc:<nombre>", "subject": "<Model:name>", "applies": false, "reason": "subject" | "where", "detail": "<texto>"}: reason subject cuando el documento no esta en la familia del sujeto (detail = la expresion subject de la regla); reason where cuando el where da false o incomplete (detail = la clause del where que decidio). Sin clave finding.
p4 (Finding.subject y document): subject = el Model:name del documento (con prefijo <store>: si viene de un store enlazado, como en GO05 H11); document = la ruta del documento relativa a la raiz del proyecto, como la guarda el registro.

PRECISIONES (cold-bundle de GO06, 2026-11-06):
p5 (nombres de campo): RuleDoc tiene los campos subject, where (opcional), condition, severity (Literal "error" | "alert"), moment (Literal "on_write" | "on_transition" | "on_check") y message (opcional). Los tests de rechazo usan esos nombres: condition, where, severity, moment, subject.
p6 (nodo y clausula en el Finding): no se agrega ningun campo a core/finding.py. El nodo viaja en Finding.subject (p4: el Model:name del documento evaluado, que es el node del finding de eval) y la clausula en Finding.what (p2). "Finding con clausula y nodo" de la aceptacion se comprueba sobre esos dos campos.
p7 (forma de subject): subject es exactamente model <= X, o una conjuncion de nivel superior de terminos model <= X (familia = interseccion, rules-language.md seccion 6). Cualquier otra clausula en subject (comparaciones, caminos, or, not) la rechaza el validador del modelo; los filtros adicionales van en where.
p8 (alcance federado): las reglas son las RuleDoc del store local. rules check sin --subject recorre solo los documentos del store local (no los stores enlazados). --subject y SUBJECT de explain aceptan tambien un documento de un store enlazado (store:Model:name o su ruta) y lo evaluan.

HIPOTESIS DEL EJECUTOR (regla 6, GO06 integrado en 622da0b5): H1 arista models->store: los validadores de RuleDoc importan el parser de store/graph/language de forma diferida; declarada [allow].upward [models, store] y [[pending]] R6 en contracts/layers.toml; reparacion en drawer task-r6-bajar-el-parser-del-lenguaje-de-reglas-a-la-capa-0-para-cerrar-la-arista-models-a-store. H2 reglas y payloads se leen de la proyeccion del indice (GO04), sin re-extraer: una condicion no ve campos no proyectados; hash de regla = content_hash, sin uso hasta GO08. H3 incomplete solo aparece si una arista lleva unavailable; el indice real hoy no lo marca (H4 de rules-language), el test lo fuerza con monkeypatch de load_edge_index. H4 resolucion: el indice se carga con stores enlazados; check sin --subject recorre solo documentos locales; DOC/SUBJECT por export id y si no por runtime_document (name, Model/name, ruta, alias:ruta); RULE solo reglas locales; "rule" en explain es RuleDoc:<nombre>. H5 sldb docs track no comprueba que los modelos del subject esten registrados (solo validacion pydantic): una regla asi no aplica a nada. H6 rules check/explain imprimen texto por defecto; el data de p1/p3 requiere --format json (o yaml); rules check --format json da {findings: [...]}. H7 where y message son str = "" (no None) por round-trip del template; condition vacia se rechaza. H8 subject entre parentesis se acepta como conjuncion. DESVIOS: api/rules/rule_graph.py y rule_writes.py nuevos (clean code); cli/parsers/public.py en vez de parsers/__init__.py (el registro vive ahi); rutas de escritura api/documents/create_document.py, api/documents/payload_save.py y cli/commands/doc.py llaman a refuse_unknown_family antes de escribir.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO06 scope): Modelo RuleDoc: sujeto = familia de modelo (expresión model <= X, resuelta con la herencia de modelos ya existente en sldb: base_models del registro, la misma que usan source_types y target_types de RelationTypeDoc) más un campo where opcional (predicado en el lenguaje, evaluado sobre cada candidato antes de la condición; false o incomplete = la regla no aplica a ese documento); condición (campo condition); severidad (error | alert); momento (on_write | on_transition | on_check); message opcional (si existe, Finding.what = message seguido de la explicación de GO02; si no, solo la explicación). Validación al escribir una RuleDoc: condition y where parsean, severidad y momento están en su vocabulario, el sujeto resuelve a un modelo registrado; cualquier fallo rechaza la escritura con el error. Registro como cualquier documento. Comando sldb rules check [--subject DOC]: con --subject evalúa sobre ese documento todas las reglas cuyo sujeto lo incluye, de cualquier momento; sin --subject evalúa todas las reglas on_check sobre todos los documentos de su familia. Emite Finding (src/sldb/core/finding.py: level, code, subject, what, fix, document) por el canal existente: level = severidad de la regla, code = rules/<nombre de la RuleDoc>, subject = el documento, what = message seguido de la explicación de GO02 (o solo la explicación si no hay message), fix = "" (la regla no prescribe remedio), document = ruta del documento sujeto. El sujeto se guarda en el campo subject como string con la expresión del lenguaje (p. ej. "model <= TaskDoc"), validada al escribir como cualquier predicado. rules check convierte a Finding de core solo los resultados false e incomplete: false → level = severidad de la regla, code rules/<nombre>; incomplete → level alert, code rules/<nombre>/incomplete, sin importar la severidad. Exit 1 si hay al menos un Finding error, 0 en otro caso (los alerts nunca fallan). DOC en --subject y SUBJECT en explain aceptan Model:name o ruta; RULE acepta RuleDoc:<nombre>, <nombre> o ruta. Una referencia que no resuelve (documento o regla) es el error existente de documento desconocido de sldb, con su exit y mensaje. Una RuleDoc mal formada se rechaza con el error de validación existente al escribir documentos (el ValidationError del modelo en el envelope, con el campo y el motivo). sldb rules explain RULE SUBJECT imprime en el envelope el finding de eval tal como lo define GO02 (node, holds, clause, seen), también cuando holds es true; exit 0 si true, 1 si false, 2 si incomplete, 3 si la regla no aplica al sujeto (familia o where), con solo el motivo en el envelope y sin finding de eval; la severidad no afecta el exit. Hash de regla = content_hash del RuleDoc; GO08 lo incluye en la clave de su caché derivada. docs/opsys/bridge_primitives/README.md: la sección Constraint se marca como reemplazada por RuleDoc con enlace a rules.md. ACEPTACION: En un store temporal con modelos Base, X < Base, Y < X y Z < Base, una RuleDoc con sujeto model <= X aplica a X e Y y no a Z; rules check reporta error y alert como Finding con cláusula y nodo, con exit 1 solo ante error; rules check sin --subject recorre solo on_check; --subject acepta Model:name y ruta; rules explain devuelve el finding de eval y los exits 0/1/2, y exit 3 con una regla cuyo where excluye al documento; un resultado incomplete en rules check sale como alert rules/<nombre>/incomplete; una regla mal formada en condition, where, severidad, momento o sujeto es rechazada al escribirla con el error correspondiente; documentación en docs/architecture/rules.md; CHANGELOG. OUTPUT_SCOPE: src/sldb/models/rule_doc.py, src/sldb/api/rules/, src/sldb/cli/commands/rules.py, docs/architecture/rules.md, docs/opsys/bridge_primitives/README.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis, no inventar API). Lenguaje: docs/architecture/rules-language.md; costura: docs/architecture/graph-backend.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_rules.py sin fallos ni saltados
- store temporal Base, X < Base, Y < X, Z < Base: RuleDoc con sujeto model <= X aplica a X e Y y no a Z
- rules check: Finding error/alert con clausula y nodo; exit 1 solo ante error; sin --subject solo on_check; --subject por Model:name y por ruta; incomplete como alert rules/<nombre>/incomplete
- rules explain: finding de eval y exits 0/1/2; exit 3 con una regla cuyo where excluye al documento
- RuleDoc mal formada (condition, where, severidad, momento, sujeto) rechazada al escribir, un test de rechazo por campo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)
- RESULTADO (coordinador 1, 2026-11-06, sobre 622da0b5 rebaseado en 289ec6c7): tests dirigidos 1179 passed, 0 skipped, 0 xfailed (test_rules 13, clean_code_rules, store_seams, CLI handler/envelope/format/v2, spec GO02, predicate_language, rutas de escritura, notations); tools/check_layers.py PASS con R6 declarada. Suite completa pendiente del supervisor.

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO06 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

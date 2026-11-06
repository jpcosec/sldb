---
id: task-go08-evaluacion-en-escritura-transicion-y-check-incremental-y-a-punto-fijo
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
- pytest tests/api/test_rules_evaluation.py
- tests/api/test_rules_evaluation.py
- tests/api/test_rules_end_to_end.py
- 3af872e77321676bc11d03be3f41fe8da40da412
- desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md
- desk/drawer/tasks/task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/payload_save_steps.py
- src/sldb/api/documents/payload_save.py
- src/sldb/api/rules/__init__.py
- src/sldb/api/rules/rules_on_write.py
- src/sldb/api/rules/rules_on_transition.py
- src/sldb/api/rules/rules_on_check.py
- src/sldb/api/rules/rule_cache.py
- src/sldb/api/rules/dirty_set.py
- src/sldb/api/rules/fixpoint.py
- src/sldb/api/rules/rule_graph.py
- src/sldb/api/edges/edges_holding.py
- src/sldb/api/edges/edges_blocked.py
- src/sldb/api/__init__.py
- src/sldb/store/models/edge_record.py
- src/sldb/api/stores/store_check.py
- src/sldb/cli/commands/stores.py
- src/sldb/store/edge_index/validation.py
- src/sldb/cli/commands/edges.py
- contracts/layers.toml
- docs/architecture/rules.md
- CHANGELOG.md
- tests/api/test_rules_evaluation.py
- tests/api/test_rules_end_to_end.py
- src/sldb/cli/error_types.py
- src/sldb/api/documents/doc_anchor_pinning.py
- src/sldb/core/exceptions/sldb_rule_violation_error.py
- src/sldb/core/exceptions/__init__.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO08: Evaluacion en escritura, transicion y check, incremental y a punto fijo

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO08 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK04. GO06 (622da0b5) dejo RuleDoc con rules check/explain a demanda; GO07 (4d521da8) las anclas doc: con anchor_state; GO09 (33b3c7a0) los effects en edges_holding. GO08 cablea la evaluacion de reglas en los tres momentos (on_write, on_transition, on_check), con cache derivada incremental en .sldb_cache y punto fijo para reglas recursivas, y prueba el ejemplo end-to-end del plan.

## Goal

_Describe the concrete result this task must produce._

on_write en los pasos de guardado (despues del pinneado, antes de persistir: error rechaza, alert pasa y reporta); on_transition en edges_holding (findings por arista, solo alerts) y edges_blocked nueva (aristas con error); on_check en stores check junto con check_doc_anchors; cache derivada por dirty set en .sldb_cache con clave por content_hash de las reglas; punto fijo semi-naive; edges check valida condiciones; test end-to-end de tres pasos; medicion de 20 escrituras antes/despues.

## Scope

_State what is in scope and what is out of scope._

En alcance: los pasos de guardado de payload (on_write), edges_holding y edges_blocked (on_transition), stores check (on_check + check_doc_anchors), la cache derivada y el dirty set en .sldb_cache, la evaluacion a punto fijo, la validacion de condiciones en edges check, docs/architecture/rules.md (ejemplo end-to-end), CHANGELOG.md, tests. Fuera: retiro de shims (GO10), cambios al lenguaje (GO05), a RuleDoc (GO06), a las anclas (GO07) o a effects (GO09) salvo el atributo findings de EdgeRecord.

PRINCIPIO DEL DUENO (2026-11-05): invariantes de UN documento = validadores pydantic del modelo; entre documentos = RuleDoc; los tests solo prueban rechazo. Aplicado aqui: (q1) GO08 no agrega validadores de modelo: lo que evalua son RuleDoc (invariantes entre documentos). (q2) Los tests de on_write prueban el rechazo (regla error: escritura rechazada, nada persistido, explicacion en el envelope; dos reglas error: ambas en el envelope) y el paso de una alert solo en lo que la aceptacion exige (persistida y en warnings).

HEREDADO: (h1) el finding de una regla es el Finding de core con code rules/<nombre> y what segun GO06 p2; incomplete = alert rules/<nombre>/incomplete (GO06). (h2) La resolucion de reglas y sujetos es la de api/rules (GO06 H4); las reglas son las del store local. (h3) effects de GO09 no se toca; findings es un atributo nuevo de EdgeRecord que, como effects (GO09 p7), no aparece en ninguna serializacion mientras no tiene valor. (h4) check_doc_anchors(store, pythonpath=None) de GO07 da las alertas anchors/doc_* y anchors/provenance_*. (h5) La medicion de 20 escrituras usa como antes el commit de cierre de GO09 (d39bf915) y como despues el de GO08.

PRECISIONES (preflight de GO08, 2026-11-06):
p1 (punto de on_write y envelope): on_write corre como un paso propio de payload_save_steps inmediatamente despues del paso de pinneado de GO07 (api/documents/doc_anchor_pinning.py) y antes del primer paso que escribe a disco; recibe el payload ya pinneado. Si hay al menos un finding error, el paso levanta un error nuevo de sldb con tipo de envelope "rules/violation" (registrado en src/sldb/cli/error_types.py, exit 1) cuyo message tiene una linea por finding error (su what, precedido por su code), ordenadas por el export id de la RuleDoc; nada se escribe. Los alerts salen siempre por sldb.cli.alert_sink (warnings del envelope), tanto si la escritura pasa como si se rechaza. No hay envelope intermedio.
p2 (cache fisica): vive en <.sldb_cache>/rules/ del store (layout.cache_dir), en JSON: un archivo por regla nombrado por su content_hash con el mapa export_id -> finding (o null si cumple), y dirty.json con el dirty set. Se lee y escribe dentro del mismo bloqueo de store que ya protege las escrituras (store/busy); no se agrega bloqueo nuevo. Un archivo ausente, ilegible o de una version distinta cuenta como cache ausente (todo dirty); la cache nunca es autoridad.
p3 (punto fijo): el lenguaje no referencia resultados de otras reglas, asi que los unicos hechos derivados son los conjuntos alcanzados por la clausura + . El punto fijo es la clausura semi-naive: se itera solo sobre los nodos nuevos de la ronda anterior (delta) hasta que una ronda no agrega nodos; un nodo ya visto no se vuelve a expandir, por eso termina con ciclos. Si el evaluador de GO05 ya lo hace asi, GO08 lo reutiliza y lo prueba con el ciclo A->B->C->A; los conjuntos viven en memoria durante la evaluacion y nunca se persisten.
p4 (ejemplo end-to-end): el fixture es el del Scope del nodo (store temporal; Task con __contract__ = [title, goal]; Review con __doc_anchors__ = [subject] y campo verdict; RuleDoc on_transition sobre model <= Task con condition any(^subject: anchor_state = "intact" and verdict = "accepted") y severity error), mas dos estados y un RelationDoc de transicion entre ellos sin condition. Paso 1: Task sin Review -> la arista no esta en edges_holding y si en edges_blocked con un finding cuyo what contiene la clausula any(...). Paso 2: Review accepted con subject doc:Task:<t> pinneada -> la arista esta en edges_holding. Paso 3: editar goal de la Task -> la arista vuelve a edges_blocked y el seen del finding muestra anchor_state = changed.
p5 (medicion): documento = desk/tasks/task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.md de este repo (existe en d39bf915 y en main). Metodo: en un worktree desechable por commit (antes = d39bf915, despues = el squash de GO08) bajo /dev/shm, tras sldb stores build, 1 escritura de calentamiento no contada y luego 20 llamadas a sldb.api save_document_payload que alternan el campo summary entre dos valores; mediana del tiempo de pared en ms con dos decimales; se registra con fecha, host y load average en el reporte (el coordinador la pasa a Validation).

PRECISIONES (cold-bundle de GO08, 2026-11-06):
p6 (excepcion): SLDBRuleViolationError en src/sldb/core/exceptions/sldb_rule_violation_error.py, subclase de SLDBError (core/exceptions/sldb_error.py), exportada desde sldb.core.exceptions como las demas; lleva la lista de Finding error en un atributo findings y su str es el message de p1. cli/error_types.py la mapea a "rules/violation" con exit 1, como mapea las otras excepciones de sldb.
p7 (edges_blocked): vive en src/sldb/api/edges/edges_blocked.py (ya en files) y se exporta desde sldb.api junto a edges_holding, con la misma firma de entrada (store, node, subject, y los mismos opcionales de edges_holding).
p8 (recalculos contados): un recalculo es una evaluacion de una regla sobre un documento que no sale de la cache (una llamada al evaluador por par regla-documento). El ejecutor concentra esa evaluacion en una sola funcion y el test la cuenta con monkeypatch. check_doc_anchors (GO07) no se cachea y no cuenta como recalculo.
p9 (despues de la medicion): "despues" es la punta de wt/go08 al terminar el trabajo (mismo arbol que el squash); el reporte nombra ese sha y el coordinador registra los dos numeros en Validation al integrar.

HIPOTESIS DEL EJECUTOR (regla 6, GO08 integrado en 3af872e7): H1 testigo: un any falso tiene seen {} (GO05 H16), asi que what agrega " (witness: <Model:name> <seen>)": primer elemento que falsea un all, primero que cumple el any interno de un none, primero alcanzado de un any falso, primero incompleto; tambien en rules check (cambia el what de GO06 p2 solo con ese sufijo). H2 las alerts de on_write viajan por sldb.core.finding_route; solo la CLI instala alert_sink; por la API sin listener se pierden -> drawer task-on-write-alerts-sin-listener-se-pierden-por-la-api-y-la-regla-ve-las-aristas-previas-a-la-escritura. H3 on_write lee el payload pinneado pero las aristas del indice previo a la escritura (misma drawer task). H4 edges_holding/edges_blocked aceptan document= opcional (el sujeto); sin el no corre ninguna regla y findings es None (fuera del dump); los findings son del sujeto y valen para todas las aristas que salen del estado; edges show --holds-for DOC ahora incluye findings: []. H5 CORREGIDO: on_write resuelve la familia de un documento aun no indexado con indexed_model_bases. H6 cada resultado en cache guarda un stamp (source_hash y payload compuesto del documento y vecinos, o del store para reglas anchas); las reglas anchas (clausura +, camino de varios pasos, cuantificador anidado) recalculan su familia si el dirty set no esta vacio. H7 solo save_document_payload corre on_write y marca el dirty set; create_document, docs track y borrado no (los cubren los stamps). H8 los findings on_check y de anclas entran en all_findings despues de judged con su nivel, sin pasar por la politica (afectan check_store, /stores/check y lint); stores check toma store_lock(wait=True). DESVIOS: core/finding_route.py nuevo (la API no importa cli); cli/alert_sink.py gana install() y cli/main.py lo llama; api/rules/rules_check.py agrega el testigo; fixpoint.py contiene el testigo (el punto fijo es la clausura semi-naive de GO05); doc_anchor_pinning.py, cli/commands/stores.py y contracts/layers.toml sin tocar.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO08 scope): on_write: en los pasos de guardado de payload, después del pinneado de anclas (GO07) y antes de persistir, de modo que la regla ve el valor pinneado; una regla error rechaza la escritura con la explicación en el envelope y nada queda escrito; una alert deja pasar y reporta. on_transition: edges_holding evalúa las reglas on_transition aplicables al sujeto que recibe (el documento que transiciona, el mismo payload sobre el que evalúa las condiciones; los extremos de la arista son estados, no sujetos) y agrega la clave findings a su resultado (la clave effects es de GO09 y no se toca); forma del resultado: edges_holding sigue devolviendo la lista de aristas que se cumplen, cada EdgeRecord con su atributo effects (GO09) y un atributo findings (lista de Finding, solo alerts); una arista con un finding error no se cumple y no aparece ahí: la devuelve la función nueva edges_blocked(store, node, subject) como lista de EdgeRecord con atributo findings (todos los de esa arista, errores y alerts). on_check: stores check evalúa todas las on_check del store y además invoca check_doc_anchors de GO07; un error hace exit 1 como los errores existentes de stores check, un alert exit 0. Canal: todo finding sale como Finding por el alert_sink, es decir en la lista warnings del envelope los alerts y en errors los errores; en on_write el envelope lleva la lista completa de findings de la escritura, ordenados por el nombre de la RuleDoc (su export id). Caché derivada y dirty set viven en .sldb_cache (regenerables, nunca autoridad; por eso el gate G_OPS_PREREQ), por store. Dirty set: al escribir o borrar un documento D entran D y todo documento con una arista entrante o saliente hacia D en el índice (vecinos a un salto: cubre anclas y caminos de un paso); una regla con clausura (+) o un cambio del content_hash de una regla invalidan toda la familia de esa regla (todos los documentos de model <= X, sin aplicar where); se vacía al terminar la evaluación. Evaluar una regla sobre un documento fuera del dirty set devuelve el resultado cacheado sin recalcular; un documento sin entrada en la caché (primer arranque, caché borrada, regla nueva) cuenta como dirty y se recalcula; con la caché ausente, todo el store es el dirty set inicial. Así stores check evalúa todas las on_check y solo recalcula las del dirty set. Caché derivada por dirty set (definido arriba) cuya clave incluye los content_hash de las reglas (GO06); hechos derivados a punto fijo (semi-naive) para reglas recursivas; nunca persistidos. edges check valida que toda condición de arista parsee. Ejemplo end-to-end (el de ROOT), como test de integración y documentado en rules.md: store temporal con modelos Task (__contract__: title, goal) y Review (__doc_anchors__: subject; campo verdict); regla on_transition sobre Task: any(^subject: anchor_state = "intact" and verdict = "accepted"); escenario: Task sin Review → la transición no aplica y el finding nombra la cláusula any(...); con Review accepted pinneada → aplica; editar goal de la Task → el ancla queda changed → vuelve a no aplicar con explicación anchor_state = changed. Medición: 20 escrituras de un TaskDoc del store de este repo, mediana del tiempo de pared, en el commit de cierre de GO09 (antes) y en el de GO08 (después), registradas en la sección Validation del TaskDoc. ACEPTACION: Escritura que viola una regla error: rechazada, nada persistido, explicación en el envelope; alert: persistida y reportada en warnings; dos reglas error violadas aparecen ambas en el envelope; edges_holding devuelve cada arista cumplida con effects intactos y findings (alerts) por arista, y una regla error saca la arista de edges_holding y la hace aparecer en edges_blocked con su finding; stores check reporta los findings on_check y las anclas doc:, con exit 1 solo ante error; incrementalidad: tras evaluar, una segunda evaluación sin cambios devuelve los mismos findings sin recalcular ningún documento (recálculos contados en el test = 0) y cambiar una regla invalida la caché de su familia; borrar .sldb_cache y reevaluar da los mismos findings; grafo de prueba A→B→C→A con una regla all(depends_on+: status = "closed") sobre A: con C abierto falla nombrando C, con todos cerrados cumple, y la evaluación termina pese al ciclo; edges check falla ante una condición mal formada; el test de integración end-to-end pasa en sus tres pasos; medición registrada; CHANGELOG. OUTPUT_SCOPE: src/sldb/api/documents/payload_save_steps.py, src/sldb/api/edges/edges_holding.py, src/sldb/api/stores/, src/sldb/cli/commands/stores*.py, src/sldb/store/edge_index/validation.py, src/sldb/cli/commands/edges.py, docs/architecture/rules.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla (la cache es derivada y regenerable); regla 6: ante un contrato ausente registrar la hipotesis, no inventar API; regla 8: la medicion va en Validation con unidad, metodo y fecha). Reglas: docs/architecture/rules.md (GO06); anclas: anchoring.md (GO07); aristas: edges.md (GO09).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_rules_evaluation.py tests/api/test_rules_end_to_end.py sin fallos ni saltados
- on_write: regla error rechaza sin persistir con explicacion en el envelope; alert persiste y sale en warnings; dos reglas error ambas en el envelope
- edges_holding: effects intactos y findings (alerts) por arista; una regla error saca la arista y la pone en edges_blocked con su finding
- stores check: findings on_check y anclas doc:, exit 1 solo ante error
- incrementalidad: segunda evaluacion sin cambios con 0 recalculos contados; cambiar una regla invalida la cache de su familia; borrar .sldb_cache y reevaluar da los mismos findings
- ciclo A->B->C->A con all(depends_on+: status = "closed") sobre A: falla nombrando C, cumple con todos cerrados, termina
- edges check falla ante una condicion mal formada
- test end-to-end de tres pasos
- medicion: 20 escrituras de un TaskDoc de este repo, mediana de tiempo de pared, antes (d39bf915) y despues, en Validation
- tests existentes de rules, edges_holding, edge_effects, doc_anchors, stores check y payload_save sin cambios
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde y tools/check_layers.py PASS
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)
- MEDICION (regla 8, 2026-11-06, host server, metodo p5: worktree desechable en /dev/shm tras sldb stores build, 1 escritura de calentamiento no contada y 20 save_document_payload alternando summary de desk/tasks/task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.md, mediana de tiempo de pared con perf_counter): antes d39bf915 = 86.48 ms (load 5.22/6.10/8.87, 18:29); despues 547a5036 (punta de wt/go08) = 89.34 ms (load 5.32/6.15/8.94, 18:28); +2.86 ms. Una corrida previa de antes con load ~10 dio 132.78 ms (ruido). RuleDoc no esta registrado en este store: on_write solo cuesta has_rules. stores build salio con exit 1 en ambos worktrees por archivos no declarados (90) o ausentes (6) del repo; el store quedo construido.
- RESULTADO (coordinador 1, 2026-11-07, sobre 3af872e7 rebaseado tras GD23/GD24/GD26): tests dirigidos 1182 passed, 7 skipped ambientales (tree-sitter en test_anchors), 0 xfailed; incluye test_rules_evaluation, test_rules_end_to_end, rules, edge_effects, doc_anchors, stores check, api documents, envelope, lenguaje, clean_code_rules y store_seams; ademas 126 passed en los tests de GD23/GD24/GD26; check_layers PASS. H5 (familia de un documento aun no indexado) corregido antes de integrar con test_a_document_not_yet_indexed_is_refused_by_a_rule_on_its_base_family. Suite completa pendiente del supervisor.

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO08 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

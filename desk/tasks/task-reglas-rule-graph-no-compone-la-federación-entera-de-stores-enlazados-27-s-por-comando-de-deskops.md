---
sldb:
  by: agent
  at: '2026-11-10T03:35:35Z'
  authority: generated
  via: save_document_payload
id: task-reglas-rule-graph-no-compone-la-federación-entera-de-stores-enlazados-27-s-por-comando-de-deskops
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
- src/sldb/api/rules/
- src/sldb/store/edge_index/
- tests/api/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rule-graph-compone-la-federaci-n-entera-de-stores-enlazados-en-cada-llamada-27-s-por-comando-de-deskops.md
---

# reglas: rule_graph no compone la federación entera de stores enlazados (27 s por comando de deskops)

## Rationale

_Explain why this task exists or the business driver behind it._

Hallazgo de la tarea de rendimiento de deskops (wt/perf-cli 7cf821f3), que bloquea el CI verde de deskops (timeouts) y la velocidad de todos los workers. Nota de deskops promovida a este drawer. rule_graph compone la federación entera de stores enlazados (unos 29 000 nodos) en cada llamada para evaluar reglas de documentos locales: 27 s en frío contra 0,27 s sin enlazados.

## Goal

_Describe the concrete result this task must produce._

La evaluación de reglas (on_write, on_transition, edges_holding/edges_blocked, rules check/explain) no compone la federación entera de stores enlazados salvo que una regla lo necesite. Los findings quedan idénticos a los de hoy, y un comando de deskops sobre el desk de deskops vuelve a tardar del orden de 1-2 s.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/rules/ (rule_graph y quien lo llame), la composición del edge index si hace falta (src/sldb/store/edge_index/), tests/api/ y CHANGELOG.md. Fuera: la semántica del lenguaje de reglas, la transacción, el resto de load_edge_index para otros consumidores (graph project, serve) salvo lo mínimo, y deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (sldb origin/main 37359542): src/sldb/api/rules/rule_graph.py:84 rule_graph(store) llama load_edge_index(store, True), que compone los stores enlazados; carga la proyección de cada documento en el backend y además llama load_edge_index(store, False) para la lista de documentos locales. Lo llaman las reglas on_write (rules_on_write.check_on_write), on_transition (rules_on_transition, edges_holding/edges_blocked), rules check y rules explain.

PRECISIONES (coordinador del plan de deskops, 2026-11-10; decisión revisable):
s1 (medición antes y después): con el store del desk de deskops (copia en /dev/shm de ~/proyectos/SLDB_1/deskops/.sldb con sus enlaces) medir rule_graph frío y caliente, load_edge_index(True/False) y el número de nodos, y un comando de deskops (deskops show task <una tarea> --root <copia>) con PYTHONPATH a esta rama. Antes: 27 s frío. Objetivo: rule_graph < 1 s y el comando de deskops < 2 s.
s2 (diseño, a elegir por el worker y explicado en el informe): (a) componer los stores enlazados solo si alguna regla del store tiene un camino que puede salir del store; si todas las reglas son locales, se usa load_edge_index(store, False). (b) Componer solo los documentos enlazados que los documentos locales referencian (vecinos a un paso o el cierre de los caminos de las reglas), sin cargar la federación entera. (c) Una caché en disco del índice compuesto, invalidada por las firmas de los shards de cada store. La preferida es (a) o (b), porque son correctas por construcción. (c) solo si (a) y (b) no alcanzan, con invalidación probada.
s3 (findings idénticos): sobre copias de los stores de los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), sldb rules check sin --subject y rules explain de las reglas de activación de deskops sobre cada tarea activa dan exactamente lo mismo antes y después. Un test nuevo fija un caso con un camino de regla que cruza a un store enlazado: tiene que seguir viéndolo.
s4 (tests, de a uno): el test nuevo, tests/api/test_rules_evaluation.py, tests/api/test_transaction.py, tests/api/test_transaction_rules_dirty.py, tests/test_rules_language_spec.py y tests/test_clean_code_rules.py. Prueba del consumidor: con deskops main (copia en /dev/shm) y PYTHONPATH a esta rama de sldb, tests/test_activation_rules.py y tests/test_lifecycle_end_to_end.py de deskops pasan enteros, cada uno en menos de 90 s.
s5 (sin tocar deskops): el arreglo es de sldb. El worker no escribe en deskops.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-10):
b1 (cierre de caminos, opción b): el conjunto de documentos que una regla puede visitar siguiendo sus pasos de camino (campos de referencia y aristas inversas ^campo) desde los documentos locales del subject, en la cantidad de saltos que la regla escribe; con + (clausura) son todos los alcanzables. En la práctica, los documentos enlazados que referencian o son referenciados por un documento local en las relaciones que nombran las reglas.
b2 (análisis estático, opción a): recorrer el AST de cada RuleDoc del store (el parser ya existe: sldb.store.graph.language.predicate_parser y predicate_ast.children, que usa dirty_set.wide) y juntar los nombres de relación/campo de sus pasos. Si ninguno de esos campos de los documentos locales apunta a un documento de un store enlazado (los ids con alias:Model:name en el índice local), la evaluación es local. Ante la duda, compone: debe ser correcto antes que rápido.
b3 (firmas, opción c): solo si a y b no alcanzan. La firma es la de shards que ya usa sldb para invalidar (live_stale / runtime_cache); el worker la reusa y no inventa una.
b4 (comando y copia de s1): la copia es /dev/shm/sldb-rg-desk, copiando ~/proyectos/SLDB_1/deskops/desk y .sldb, más los stores enlazados que nombra su store.yaml en sus rutas (o copias en /dev/shm/sldb-rg-<alias> con el store.yaml de la copia reapuntado). La tarea es la primera de deskops list tasks en esa copia. El comando: deskops show task <id> --root /dev/shm/sldb-rg-desk con PYTHONPATH a esta rama de sldb.
b5 (copias de los 6 desks): /dev/shm/sldb-rg-6/<desk> (deskops, sldb, spec2viz, scion, pron, graph_ui), desk/ y .sldb/ de cada uno desde ~/proyectos/SLDB_1/<desk> y UIs/graph_ui. Se borran al terminar.
b6 («salvo lo mínimo»): load_edge_index no cambia de firma ni de comportamiento para otros consumidores. Si el arreglo necesita una variante (por ejemplo, componer solo un conjunto de ids), se agrega como parámetro opcional con default igual a hoy o como función nueva.

## Validation

_List the checks required before this task can close._

- Tabla de tiempos antes y después (s1)
- Findings idénticos en los 6 desks y test de camino cruzado (s3)
- Tests de sldb de s4 de a uno
- deskops test_activation_rules y test_lifecycle_end_to_end contra esta rama, menos de 90 s cada uno

## Done When

_Name the observable condition that makes the task complete._

rule_graph no compone la federación entera cuando las reglas no la necesitan: los findings en los 6 desks son idénticos y el test de camino cruzado queda verde. La tabla de tiempos antes y después muestra rule_graph < 1 s y el comando de deskops < 2 s. Los tests de sldb de s4 están verdes, y test_activation_rules y test_lifecycle_end_to_end de deskops pasan contra esta rama en menos de 90 s cada uno. CHANGELOG.

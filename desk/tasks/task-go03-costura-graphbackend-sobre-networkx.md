---
id: task-go03-costura-graphbackend-sobre-networkx
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
- src/sldb/store/graph/backend/__init__.py
- src/sldb/store/graph/backend/protocol.py
- src/sldb/store/graph/backend/networkx_backend.py
- src/sldb/api/graph/analyze.py
- src/sldb/api/graph/__init__.py
- src/sldb/cli/parsers/graph_analysis.py
- src/sldb/cli/commands/graph_analysis.py
- src/sldb/api/stores/store_declaration.py
- docs/architecture/graph-backend.md
- CHANGELOG.md
- tests/store/test_graph_backend.py
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# GO03: Costura GraphBackend sobre networkx

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO03 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9). D5 (networkx tras una costura GraphBackend, sin Neo4j ahora) confirmada por el dueno el 2026-11-04. Produce el gate G_SEAM; GO04 y GO05 se apoyan en la costura.

## Goal

_Describe the concrete result this task must produce._

Protocolo GraphBackend (load, eval, analyze) con implementacion networkx; los seis comandos graph y api/graph enrutados por analyze sin cambiar salidas; eval sobre el subconjunto de GO02 sin caminos; clave graph_backend en store.yaml; docs/architecture/graph-backend.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/graph/backend* (nuevo), src/sldb/api/graph/, src/sldb/cli/parsers/graph_analysis.py y src/sldb/cli/commands/graph_analysis.py, la carga de store.yaml (src/sldb/api/stores/store_declaration.py) para graph_backend, docs/architecture/graph-backend.md, CHANGELOG.md, tests. Fuera: caminos y cuantificadores en eval (GO05), proyeccion real (GO04), cualquier motor distinto de networkx. Leer antes: docs/architecture/rules-language.md, src/sldb/store/edge_index/compose.py, src/sldb/store/graph/analysis/, src/sldb/api/graph/analyze.py y __init__.py, src/sldb/cli/commands/graph_analysis.py, src/sldb/cli/serve/graph_routes.py, src/sldb/store/query_engine/where_parse.py, where_subject.py, src/sldb/api/stores/store_declaration.py, tests/store/test_graph_analysis.py, tests/api/test_api_graph_analysis.py, tests/api/test_api_graph.py. PRECISIONES tras preflight (2026-11-04): (p1) goldens: hoy no existen; el primer commit del ejecutor, antes de tocar src/, los captura desde el codigo de main corriendo los seis comandos sldb graph (path, cycles, order, components, central, similar) con su salida por defecto de hoy (stdout tal cual; los comandos graph no tienen --format json) sobre el store que construye la fixture world de tests/api/test_api_graph_analysis.py (cadena 3->2->1 mas un spec aislado), y los guarda en tests/fixtures/graph_goldens/<comando>.txt; un test compara la salida posterior byte a byte con esos archivos. (p2) indice compuesto del propio repo = compose_edge_index(<raiz del repo>/.sldb) de src/sldb/store/edge_index/compose.py; el test lo carga en el backend con load(indice, None). (p3) inventario de api/graph cubierto por el espia: las diez funciones de src/sldb/api/graph/analyze.py (graph_path, graph_paths, graph_cycles, graph_order, graph_layers, graph_components, graph_islands, graph_isolated, graph_central, graph_similar) y los seis subcomandos de src/sldb/cli/parsers/graph_analysis.py; execute.py, neighborhood.py, snapshot.py y traverse.py quedan fuera. (p4) forma del finding de GO02 (docs/architecture/rules-language.md seccion 4 y 6): claves node, holds (true/false/incomplete), clause, seen (mapa campo -> valor leido). PRECISIONES tras cold-bundle (2026-11-05): (p5) el protocolo GraphBackend tiene tres operaciones, load, eval y analyze, como fija dag.yaml; la mencion '(load, eval)' del brief del plan es un resumen y no restringe; analyze se documenta y se prueba. (p6) la lista files de este TaskDoc manda sobre output_scope de dag.yaml: src/sldb/cli/commands/graph_analysis.py y src/sldb/api/stores/store_declaration.py estan permitidos (enrutar los comandos y leer graph_backend). (p7) argumentos fijos de los goldens, los mismos que ya usa tests/api/test_api_graph_analysis.py:90 sobre la fixture world: graph path sldb://document/Spec:s3 sldb://document/Spec:s1; graph cycles; graph order; graph components; graph central --kind degree; graph similar sldb://document/Spec:s1.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO03 scope): Protocolo GraphBackend con tres operaciones: load(índice compuesto, proyección), eval(predicado parseado, sujeto opcional) → findings, y analyze(op, args) → resultado, donde op es uno de path, cycles, order, components, central, similar con los argumentos que hoy reciben; el backend nunca expone su grafo interno. Índice compuesto = el objeto que hoy devuelve compose (store/edge_index/compose.py: nodos y aristas ya resueltos); compose queda fuera del backend y le entrega ese objeto; load lo guarda en la instancia y devuelve None. Proyección = mapa export_id → facet payload o None; load la guarda; eval la lee cuando el sujeto se pasa como export_id (si no hay proyección o el id no está en ella, eval levanta ValueError "sin proyección para <id>") y usa el payload cuando el sujeto se pasa como payload; en GO03 la proyección real es siempre None (GO04 la produce), así que los tests de GO03 pasan el sujeto como payload. Implementación networkx que envuelve el análisis de grafo actual (lo que hoy corre sobre networkx) sobre el índice recibido; los seis comandos graph y la API api/graph llaman a analyze, sin cambiar ninguna salida. eval en este nodo acepta exactamente el subconjunto de GO02 sin caminos (has, nonempty, in, ~, model <=, comparaciones, and/or/not, paréntesis, sustitución {campo} desde el sujeto) evaluado sobre la facet del sujeto si el sujeto es un export_id con proyección cargada, o sobre el payload pasado; un predicado con camino levanta NotImplementedError hasta GO05. Selección por la clave graph_backend de store.yaml: un escalar string; admitidos en esta fase solo "networkx"; ausente = networkx; otro valor = error al cargar el store con el mensaje graph_backend <valor> no admitido; admitidos: ["networkx"]. El backend espía de los tests se inyecta por Python (una instancia pasada a las funciones de api/graph y a la carga del store en el test), no por store.yaml. Documento docs/architecture/graph-backend.md con el protocolo y la regla: cualquier motor futuro (Kùzu, Neo4j, Datalevin) entra detrás de esta costura; las reglas no lo ven. ACEPTACION: Goldens de los seis comandos graph idénticos a antes; los tests existentes de api/graph pasan sin cambios y un test con un backend espía comprueba que cada comando graph y cada función de api/graph invocan al backend; un test carga el índice compuesto del propio repo en el backend; un test evalúa has(id) and status != "x" por eval sobre un documento y recibe un finding con la forma de GO02, y un predicado con camino levanta NotImplementedError; store.yaml sin clave carga networkx, con clave inválida falla con el mensaje definido en el scope; el protocolo está documentado; CHANGELOG. Produce G_SEAM. OUTPUT_SCOPE: src/sldb/store/graph/backend*, src/sldb/api/graph/, src/sldb/cli/parsers/graph_analysis.py, store.yaml (clave graph_backend), docs/architecture/graph-backend.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: toda capacidad nueva entra con spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis en este TaskDoc, no inventar API). Semantica de eval y forma del finding: docs/architecture/rules-language.md (GO02, en main).

## Validation

_List the checks required before this task can close._

- pytest -k 'graph or backend or store_declaration' -q sin fallos ni saltados
- goldens de los seis comandos graph (path, cycles, order, components, central, similar) iguales antes y despues
- suite completa sin rojos

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO03 cumplida linea por linea, revision en frio aceptada, G_SEAM satisfied en dag.yaml citando el commit.

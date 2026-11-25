FILE:desk/tasks/task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3.md
---
sldb:
  by: agent
  at: '2026-11-16T16:20:43Z'
  authority: generated
  via: save_document_payload
id: task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3
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
- src/sldb/api/graph/analyze.py
- src/sldb/store/graph/backend/networkx_backend.py
- src/sldb/cli/parsers/graph_analysis.py
- src/sldb/cli/commands/graph_analysis.py
- src/sldb/cli/serve/graph_routes.py
- tests/api/test_api_graph_analysis.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Grafo: graph_path y graph_paths devuelven caminos explicados con la procedencia de cada tramo (B3)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: las reglas e impacto de specIR (IR10) deben apoyarse en sldb. Hoy graph_path y graph_paths en sldb.api.graph devuelven solo listas de ids, sin decir por qué relación ni con qué procedencia se une cada tramo.

## Goal

_Describe the concrete result this task must produce._

Caminos explicados: por cada tramo, origen, destino, tipo de relación, dirección recorrida y procedencia de la arista.

## Scope

_State what is in scope and what is out of scope._

Verificado hoy: graph_path y graph_paths (módulo analyze de sldb.api.graph) devuelven list[str]; el módulo traverse tiene solo targets, sources, children y similares sin camino. No existe pedido ni tarea previa. Añadir una variante o un parámetro que devuelva el camino explicado sin romper la forma actual (compatibilidad con la CLI de graph y sus goldens), pasar por el protocolo GraphBackend, exponerlo en la CLI y en sldb serve si ya exponen graph path. La procedencia sale de la arista del índice (RelationDoc o campo de referencia); cuando una arista tiene varias, decidir y documentar.

Precisiones (coordinador, 2026-11-16): si entre a y b hay varias aristas que pasan el filtro, se listan todas en el tramo (steps[i].edges), ordenadas por precedencia relation_doc > schema > structural > alias; una arista espejo con metadata.reverse true no se lista aparte: aparece como su arista directa con direction backward; evidence no entra en provenance. La forma sin explain no cambia.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un módulo nuevo path_steps.py en el paquete sldb.store.graph.analysis con explain_path(index, nodes, relations, directed): por cada par consecutivo (a, b) toma las aristas a->b (direction forward) o b->a (direction backward) de index.edges_from/edges_to filtradas por analysis.relations.resolve(index, relations) y emite {source, target, relation, direction, provenance}. provenance = {origin, relation_doc o field, from_store} tomado de EdgeRecord.metadata. 2) Registrar las operaciones path_explained y paths_explained en _OPERATIONS de src/sldb/store/graph/backend/networkx_backend.py componiendo path_between/paths_between con explain_path; las operaciones path y paths no cambian (goldens intactos). 3) src/sldb/api/graph/analyze.py: graph_path y graph_paths ganan explain: bool = False que elige la operación. 4) CLI --explain en src/sldb/cli/parsers/graph_analysis.py y su manejo en src/sldb/cli/commands/graph_analysis.py (70 líneas: la impresión va a un módulo nuevo); sldb serve: path_payload acepta ?explain=1 y agrega steps junto a path. 5) Tests en tests/api/test_api_graph_analysis.py (AnalysisWorld y el índice del propio repo).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_graph_backend.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; graph_path(..., explain=True) sobre el índice del propio repo devuelve tramos con origin y relation_doc o field; los goldens de tests/fixtures/graph_goldens/ no cambian; `sldb graph path --explain` y GET con ?explain=1 lo exponen; CHANGELOG y commit; aviso a IR anotado en result-summary.md.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-grafo-graph-path-y-graph-paths-devuelven-caminos-explicados-con-la-procedencia-de-cada-tramo-b3: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


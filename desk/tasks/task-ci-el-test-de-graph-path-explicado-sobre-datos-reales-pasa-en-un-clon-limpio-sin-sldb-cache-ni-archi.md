---
sldb:
  by: agent
  at: '2026-11-16T22:17:48Z'
  authority: generated
  via: save_document_payload
id: task-ci-el-test-de-graph-path-explicado-sobre-datos-reales-pasa-en-un-clon-limpio-sin-sldb-cache-ni-archi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- tests/api/test_api_graph_analysis.py
- tests/test_clean_code_rules.py
- d1942f42
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
depends_on: []
pills: []
files:
- tests/api/test_api_graph_analysis.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
---

# CI: el test de graph-path explicado sobre datos reales pasa en un clon limpio, sin .sldb_cache ni archivos generados

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de GitHub sobre c5cb52f0 falla en 3.12 y 3.13 con TypeError 'NoneType' object is not subscriptable en tests/api/test_api_graph_analysis.py::test_explain_over_the_repo_own_index_names_origin_and_relation_doc (B3). El coordinador lo reprodujo en un clon limpio: graph_path sobre el .sldb del repo devuelve None porque las aristas entre rituales viven en el índice derivado .sldb_cache (ignorado por git); tras sldb stores update el camino aparece. El test dependía de la caché del checkout local.

## Goal

_Describe the concrete result this task must produce._

El test que cubre graph_path(..., explain=True) con aristas de origin relation_doc y schema reales pasa en un clon recién hecho, sin .sldb_cache, sin knowledge/symbols generados y con XDG_CACHE_HOME vacío, y sigue pasando en el checkout de trabajo.

## Scope

_State what is in scope and what is out of scope._

Entra: reescribir ese test para que no lea el .sldb del repo. Arma en tmp_path un store propio con documentos y al menos una arista de origin relation_doc y otra de origin schema (puede reutilizar el AnalysisWorld del mismo archivo si ya las tiene, o un fixture mínimo), y comprueba la misma propiedad: cada arista de los steps trae origin y relation_doc o field. Si hace falta construir el índice, el test lo construye en tmp_path con la API pública. No entra: cambiar código de src/ (path_steps, analyze); si el test revela que el código depende de la caché para algo que no debería, se anota en result-summary.md y lo decide el coordinador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer el test y AnalysisWorld en tests/api/test_api_graph_analysis.py. 2) Reescribir el test como se describe. 3) Reproducir en un clon limpio: git clone del checkout a /dev/shm, y allí, con XDG_CACHE_HOME apuntando a un directorio vacío, correr el archivo de test con uv run --frozen --extra code --extra dev pytest -q -p no:cacheprovider. 4) Validation en el checkout de trabajo. 5) Borrar el clon de /dev/shm.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_graph_analysis.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; result-summary.md tiene la salida del archivo de test corrido en un clon limpio sin .sldb_cache y con XDG_CACHE_HOME vacío, con rc 0; commit.

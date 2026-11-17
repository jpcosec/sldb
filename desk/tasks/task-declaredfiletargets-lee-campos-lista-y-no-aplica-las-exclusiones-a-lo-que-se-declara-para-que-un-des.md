---
sldb:
  by: agent
  at: '2026-11-17T11:19:25Z'
  authority: generated
  via: create_document
id: task-declaredfiletargets-lee-campos-lista-y-no-aplica-las-exclusiones-a-lo-que-se-declara-para-que-un-des
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-080724-suggestion-project-graph-de-deskops-destinos-de-h1-que-declaredfiletargets-no-puede-declarar-y-closed-sin-cuerpo-h2.md
depends_on: []
pills: []
files:
- src/sldb/api/edges/project_graph/declared_file_targets.py
- src/sldb/api/edges/project_graph/declared_target_nodes.py
- tests/api/test_project_graph_config.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# DeclaredFileTargets lee campos lista y no aplica las exclusiones a lo que se declara, para que un destino que existe no cuente como faltante

## Rationale

_Explain why this task exists or the business driver behind it._

deskops ya declara DeclaredFileTargets(directory=desk/materializations, field=target_identity), pero 49 destinos que existen siguen como faltantes en graph missing: (1) campos lista como references (DeclaredFileTargets solo lee un valor str, declared_target_nodes.py:_field_value); (2) menciones en el cuerpo (LineMentions) a archivos del proyecto; (3) destinos declarados bajo directorios excluidos (FileExclusions los descarta aunque el campo los declara). Origen: desk/inbox/20261117-080724-suggestion-project-graph-de-deskops-destinos-de-h1-que-declaredfiletargets-no-puede-declarar-y-closed-sin-cuerpo-h2.md.

## Goal

_Describe the concrete result this task must produce._

Un destino declarado por DeclaredFileTargets, venga de un campo escalar o de un campo lista, que es un archivo existente del proyecto se vuelve nodo aunque esté bajo una exclusión; y hay una forma declarativa de que las menciones de LineMentions a archivos existentes del proyecto no cuenten como faltantes.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/api/edges/project_graph/declared_file_targets.py y declared_target_nodes.py, leer valores lista además de str y no aplicar FileExclusions a los destinos declarados explícitamente; para LineMentions, una opción de configuración del project graph (documentada) que resuelve una mención a un archivo existente como nodo de archivo; tests en tests/api/test_project_graph_config.py con los tres casos de la nota. CHANGELOG y doc del project graph. No entra: el estado en el cuerpo de los issues de deskops (H2), que deskops aceptó perder.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer declared_file_targets.py, declared_target_nodes.py, file_exclusions.py y line_mentions.py. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph_config.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a deskops.

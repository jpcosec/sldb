Task: task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización
Title: declared_target_nodes acepta un directorio existente como target declarado de una materialización
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T11:51:37Z'
  authority: generated
  via: save_document_payload
id: task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md
depends_on: []
pills: []
files:
- src/sldb/api/edges/project_graph/declared_target_nodes.py
- tests/api/test_project_graph.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# declared_target_nodes acepta un directorio existente como target declarado de una materialización

## Rationale

_Explain why this task exists or the business driver behind it._

Una MaterializationContractDoc con target_identity igual a un directorio no se convierte en nodo del grafo porque src/sldb/api/edges/project_graph/declared_target_nodes.py exige is_file(); queda como missing_declared_target y graph missing la reporta. En el cierre SV01-SV04 obligó a crear 62 materializaciones para 66 archivos. deskops ya cubre los archivos bajo un directorio por prefijo en su closeout. Origen: desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md.

## Goal

_Describe the concrete result this task must produce._

Un target declarado que es un directorio existente del proyecto produce un nodo del grafo (de directorio) y graph missing no lo reporta; un directorio inexistente sigue siendo missing.

## Scope

_State what is in scope and what is out of scope._

Entra: en declared_target_nodes.py (y file_node.py si el nodo de archivo es la base), aceptar directorios existentes con un nodo de kind directory o el equivalente que ya exista en project_graph; tests en tests/api/test_project_graph.py. CHANGELOG. No entra: expandir el directorio en un nodo por archivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer declared_target_nodes.py, declared_file_targets.py, file_node.py y file_nodes.py. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_project_graph_config.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a deskops.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-declared-target-nodes-acepta-un-directorio-existente-como-target-declarado-de-una-materialización"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.

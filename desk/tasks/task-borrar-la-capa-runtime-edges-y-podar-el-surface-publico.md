---
id: task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico
current_node: checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-execution-ready
history: []
references: []
depends_on:
- task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion
pills: []
files: []
checklists:
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-execution-ready
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-testing-ready
- checklist-task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Borrar la capa runtime/edges y podar el surface publico

## Rationale

_Explain why this task exists or the business driver behind it._

Paso final del retiro. Son ~1613 lineas en 30+ modulos. api/__init__.py se declara contrato publico para pron, kgdb y deskops, y ~20 simbolos de edges mueren (check_edges, edges_from/to, edge_node, edge_nodes_of_type, load_edge_index, init_relations, rebuild_edges, EdgeIndex, EdgeCheckReport, EdgeRebuildReport, serializers, node-id helpers). Handoff ya enviado al inbox de deskops.

## Goal

_Describe the concrete result this task must produce._

Borrar edge_sync.py, edge_rebuild.py, edge_doc_contribution.py, edge_index/doc_contribution.py, models/doc_edges.py, models/edge_contribution.py, api/edges/rebuild_edges.py, cli/commands/edges.py, cli/parsers/edges.py, cli/serve/edges_routes.py, y podar api/__init__.py.

## Scope

_State what is in scope and what is out of scope._

IN: borrado de la capa y poda del __all__. Los consumidores clase B (payload_save_steps, untrack_document, dag_writes, index_commit, selfdoc_write, derived_rebuild, export, ops) se reescriben contra el snapshot. OUT: EdgeNodeRecord/EdgeRecord SOBREVIVEN (los usa store/graph/convert.py:10-11) y los helpers node_ids se mueven a store/graph.

## Implementation Path

_Outline the expected implementation route or affected surface._

Seguir el orden de la seccion 5 del plan: ningun paso intermedio deja main roto. cli/serve/lint_routes.py:62 consume check_edges y queda huerfano: hay que reescribirlo si o si.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

pytest verde; ningun modulo de la capa edges existe; api/__init__.py sin simbolos muertos; /lint funcionando contra la capa nueva.

---
id: task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges
current_node: checklist-task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges-execution-ready
- checklist-task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges-testing-ready
- checklist-task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Dar fuente propia al grafo: store/graph deja de leer runtime/edges

## Rationale

_Explain why this task exists or the business driver behind it._

Hallazgo bloqueante de docs/architecture/edges-retirement-plan.md seccion 0: la capa NUEVA lee a la VIEJA. store/graph/ (analysis networkx, convert, executor, api.graph entero) obtiene su EdgeIndex de compose_edge_index sobre los shards de runtime/edges/ (store/edge_index/compose.py:21, compose.py:13,58; api/edges/edge_reading.py:14). Sin fuente propia, retirar edges rompe toda la capa de grafo. Este es el paso 1 y bloquea todo el retiro.

## Goal

_Describe the concrete result this task must produce._

Que store/graph/ construya su indice desde el snapshot portable (semantic export -> sldb_semantic_export_to_snapshot, graph/ingest_sldb.py:20) en vez de desde los shards de runtime/edges/.

## Scope

_State what is in scope and what is out of scope._

IN: re-puntar la fuente del EdgeIndex de la capa graph. OUT: NO borrar todavia runtime/edges/ ni sus modulos; el borrado es una tarea posterior. Los gaps G1-G5 se atacan aparte.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer docs/architecture/edges-retirement-plan.md completo antes de tocar nada. El camino ya existe: store/export.py:18,43 (sldb_kgdb_semantic_export) -> graph/ingest_sldb.py:20 -> cli/parsers/graph.py:70 (graph ingest-sldb). Hay que hacer que ese sea el input por defecto de la capa graph.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=src python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

store/graph/ no llama a compose_edge_index ni lee runtime/edges/; pytest completo en 1015 passed 0 failed; las consultas de grafo devuelven los mismos resultados que antes (paridad demostrada con evidencia, no asumida).

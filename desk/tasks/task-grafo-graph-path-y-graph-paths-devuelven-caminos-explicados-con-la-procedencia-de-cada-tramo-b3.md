---
sldb:
  by: agent
  at: '2026-11-15T15:52:49Z'
  authority: generated
  via: create_document
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
files: []
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

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q de los archivos tocados, uno a la vez
- tools/check.sh
- sldb stores build --check

## Done When

_Name the observable condition that makes the task complete._

Caminos explicados con test sobre el índice del propio repo; formas antiguas intactas; suite de a un archivo, tools/check.sh y stores build --check.

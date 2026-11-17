---
sldb:
  by: agent
  at: '2026-11-17T05:12:44Z'
  authority: generated
  via: create_document
id: task-sw11-el-panel-izquierdo-del-workbench-muestra-el-grafo-de-documentos-relacionados-con-el-abierto-al
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
- area:surface
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-011531-suggestion-sw11-panel-izquierdo-del-workbench-ver-el-grafo-de-documentos-relacionados-centrado-en-el-documento-abierto.md
depends_on: []
pills: []
files:
- surface/src/workbench/TopologyMindmap.tsx
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW11: el panel izquierdo del Workbench muestra el grafo de documentos relacionados con el abierto al centro, desde lo que entrega sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Hoy el panel dibuja el documento como raíz y solo sus piezas compuestas y las referencias que la UI parsea del payload; un documento sin composiciones queda solo. JP pidió un grafo con el documento al centro y lo que referencia y lo que lo referencia, navegable. En dos stores probados, GET /edges?id=<doc> devolvió vacío y /graph/neighborhood solo el propio nodo, aunque existe .sldb_cache/edges. Origen: desk/inbox/20261117-011531-suggestion-sw11-panel-izquierdo-del-workbench-ver-el-grafo-de-documentos-relacionados-centrado-en-el-documento-abierto.md.

## Goal

_Describe the concrete result this task must produce._

Con un documento que tiene relaciones entrantes y salientes en un store real, el panel muestra ambas con el documento al centro (1 y 2 saltos), un clic en un vecino lo abre, un documento sin relaciones lo dice, hay un tope de nodos para documentos muy referenciados, y ningún vecino sale de parseo en la UI.

## Scope

_State what is in scope and what is out of scope._

Entra: primero averiguar por qué /edges y /graph/neighborhood devuelven vacío (formato del id, índice sin construir o defecto de serve); si es de sldb serve, se crea una tarea aparte en sldb y esta queda esperándola. Después, el grafo en surface/src/workbench/TopologyMindmap.tsx desde /edges y /graph/neighborhood, quitando el parseo de referencias del payload (parseRefString), y decidiendo cómo convive con el árbol de composición (lente o pestaña); tests de vitest con el cliente inyectable. Precisión de JP: el Workbench es la UI de SLDB, general para cualquier store; la UI no calcula. No entra: copiar código de graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir el vacío de /edges con sldb serve sobre un store real. 2) Diagnosticar y, si es de serve, abrir la tarea. 3) Implementar el grafo. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; result-summary.md explica por qué /edges devolvía vacío; commit.

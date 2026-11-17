---
sldb:
  by: agent
  at: '2026-11-17T03:04:40Z'
  authority: generated
  via: save_document_payload
id: task-sw6-el-workbench-vuelve-a-la-ui-de-deskops-y-muestra-gates-y-evidencia-de-la-tarea-desde-deskops-vie
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
- desk/inbox/20261116-233905-suggestion-sw6-marco-de-deskops-2-3-4-3-5-el-workbench-se-abre-desde-la-ui-de-deskops-vuelve-a-ella-y-muestra-el-estado-de-workflow-que-entrega-deskops.md
depends_on:
- task-sw5-el-dueño-de-un-modelo-sale-de-describe-model-model-ref-y-los-modelos-de-deskops-dicen-gestionado
pills: []
files:
- surface/src/app/WorkbenchShell.tsx
- surface/src/workbench/Spec2VizInspectorView.tsx
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW6: el Workbench vuelve a la UI de deskops y muestra gates y evidencia de la tarea desde deskops view; pide a deskops y graph_ui las operaciones que faltan

## Rationale

_Explain why this task exists or the business driver behind it._

El manual (§2.1-2.3, §3.4-3.6) pide entrar y volver a la UI de deskops, mostrar lo que deskops view dice de una tarea (por ejemplo '2/2 gates ok'), listar verbos de deskops en ⌘K según deskops next y mostrar los cambios sin commitear; hoy no hay enlace de regreso, no se muestra nada de la tarea, y no existen endpoints de deskops next, de verbos aparte de advance y ack/promote, ni de git. Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233905-suggestion-sw6-marco-de-deskops-2-3-4-3-5-el-workbench-se-abre-desde-la-ui-de-deskops-vuelve-a-ella-y-muestra-el-estado-de-workflow-que-entrega-deskops.md.

## Goal

_Describe the concrete result this task must produce._

Con lo que ya existe: enlace de regreso a la UI de deskops (a la tarea si el documento abierto es un TaskDoc) y gates y evidencia de la tarea leídos de /desk/api/view/task; las operaciones que faltan quedan pedidas por nota a deskops y a graph_ui y sus controles se muestran deshabilitados con el motivo. Nada se dibuja sin fuente real.

## Scope

_State what is in scope and what is out of scope._

Entra: cortes (a) y (b) de la nota: enlace de regreso, lectura de /desk/api/view/task, controles deshabilitados con motivo, y notas a deskops (contrato deskops-ui) y a graph_ui (servidor) pidiendo deskops next, ejecución de verbos y conteo y commit de cambios; tests de vista. No entra: la paleta de verbos (corte c, cuando existan las operaciones).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer WorkbenchShell.tsx, Spec2VizInspectorView.tsx y el proxy /desk de vite. 2) Implementar (a). 3) Mandar las notas (b) con deskops message send. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; las notas a deskops y graph_ui están enviadas y citadas en result-summary.md; commit.

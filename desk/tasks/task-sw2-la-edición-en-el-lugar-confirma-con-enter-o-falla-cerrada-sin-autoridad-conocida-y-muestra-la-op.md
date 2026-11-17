---
sldb:
  by: agent
  at: '2026-11-17T02:52:51Z'
  authority: generated
  via: create_document
id: task-sw2-la-edición-en-el-lugar-confirma-con-enter-o-falla-cerrada-sin-autoridad-conocida-y-muestra-la-op
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
- desk/inbox/20261116-233721-suggestion-sw2-flujo-1-6-3-2-4-la-edici-n-en-el-lugar-confirma-falla-cerrada-y-muestra-la-operaci-n-y-su-resultado.md
depends_on: []
pills: []
files:
- surface/src/workbench/ProsaWorkbenchView.tsx
- surface/src/app/WorkbenchShell.tsx
- surface/src/react/useDocumentEditor.ts
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW2: la edición en el lugar confirma con Enter o ⌘↵, falla cerrada sin autoridad conocida y muestra la operación y su resultado con el hash al día

## Rationale

_Explain why this task exists or the business driver behind it._

En workbench/ProsaWorkbenchView.tsx: InlineEditableProse usa textarea para todo y Enter no confirma; la autoridad falla abierta (modelDetail?.authority ?? 'authored') mientras el servidor usa 'generated' por defecto; la etiqueta de operación de la lente Fierros falta en el título y en bloques transcluidos; tras guardar solo se ve 'sincronizado'; y el hash de la etiqueta queda viejo porque app/WorkbenchShell.tsx carga documents una vez (§6 Flujo 1, §3.2). Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233721-suggestion-sw2-flujo-1-6-3-2-4-la-edici-n-en-el-lugar-confirma-falla-cerrada-y-muestra-la-operaci-n-y-su-resultado.md.

## Goal

_Describe the concrete result this task must produce._

Enter confirma en campos de una línea y ⌘↵ en los de bloque; sin autoridad conocida todo es solo lectura; la etiqueta de operación (POST /save · expected <hash>) aparece también en el título y en bloques transcluidos; tras guardar se muestra el hash nuevo o el error accionable; el hash de la etiqueta coincide siempre con el expected que se envía.

## Scope

_State what is in scope and what is out of scope._

Entra: los cinco puntos de la nota en ProsaWorkbenchView.tsx, WorkbenchShell.tsx y react/useDocumentEditor.ts, con tests de vitest contra el cliente inyectable (sin mocks de módulo). No entra: verbos de deskops y 'gestionado por deskops' (SW5, SW6).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar cada punto en el código. 2) Implementar. 3) Un test por punto. 4) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con un test por cada uno de los cinco puntos; commit.

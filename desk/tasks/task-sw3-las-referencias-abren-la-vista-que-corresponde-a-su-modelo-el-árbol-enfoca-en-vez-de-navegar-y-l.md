---
sldb:
  by: agent
  at: '2026-11-17T03:03:32Z'
  authority: generated
  via: save_document_payload
id: task-sw3-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-el-árbol-enfoca-en-vez-de-navegar-y-l
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
- desk/inbox/20261116-233748-suggestion-sw3-navegaci-n-1-3-2-2-7-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-y-la-paleta-busca-por-s-mbolo-y-hash.md
depends_on:
- task-sw2-la-edición-en-el-lugar-confirma-con-enter-o-falla-cerrada-sin-autoridad-conocida-y-muestra-la-op
pills: []
files:
- surface/src/workbench/ProsaWorkbenchView.tsx
- surface/src/workbench/TopologyMindmap.tsx
- surface/src/workbench/Spec2VizInspectorView.tsx
- surface/src/app/WorkbenchShell.tsx
- surface/src/main.tsx
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW3: las referencias abren la vista que corresponde a su modelo, el árbol enfoca en vez de navegar y la paleta busca por símbolo y hash

## Rationale

_Explain why this task exists or the business driver behind it._

Las fichas de referencia (workbench/ProsaWorkbenchView.tsx, parseDocRef) siempre abren prosa aunque apunten a un diagrama o a una fuente; el clic en un nodo del árbol (TopologyMindmap.tsx) reemplaza el documento en vez de enfocar la sección; la paleta ⌘K no busca por símbolo ni hash; la tecla 3 y la pestaña Esquema no tienen salida sin modelo activo; y #/legacy se decide una sola vez al cargar (main.tsx) (§1.3, §2.2, §7). Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233748-suggestion-sw3-navegaci-n-1-3-2-2-7-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-y-la-paleta-busca-por-s-mbolo-y-hash.md.

## Goal

_Describe the concrete result this task must produce._

Un ref a un diagrama abre el Inspector y uno a una fuente abre Extracción y Anclaje (también desde los refs del Inspector); el clic en un nodo que es parte del documento abierto enfoca su bloque; ⌘K encuentra por símbolo y por hash; la tecla 3 sin modelo activo está deshabilitada con el motivo; cambiar el hash a o desde #/legacy cambia la app sin recargar.

## Scope

_State what is in scope and what is out of scope._

Entra: los cinco puntos en ProsaWorkbenchView.tsx, TopologyMindmap.tsx, Spec2VizInspectorView.tsx, WorkbenchShell.tsx y main.tsx; la vista que corresponde a un modelo se decide con lo que entrega sldb (familia o bases de describe_model), no con una lista de nombres en la UI: si falta el dato, nota a sldb; tests de ruteo por tipo de destino, de foco de sección y de búsqueda por símbolo y hash. No entra: autoridad (SW5).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar cada punto. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; commit.

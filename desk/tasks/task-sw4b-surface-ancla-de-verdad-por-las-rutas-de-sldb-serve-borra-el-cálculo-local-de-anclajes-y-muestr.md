---
sldb:
  by: agent
  at: '2026-11-17T04:06:55Z'
  authority: generated
  via: save_document_payload
id: task-sw4b-surface-ancla-de-verdad-por-las-rutas-de-sldb-serve-borra-el-cálculo-local-de-anclajes-y-muestr
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
- desk/inbox/20261116-233813-suggestion-sw4-flujo-3-6-4-anclar-de-verdad-hoy-crear-atomdoc-y-anclar-no-guarda-un-anclaje-y-el-estado-del-anclaje-se-calcula-en-la-ui.md
depends_on:
- task-sw4a-sldb-serve-expone-escribir-un-anclaje-y-leer-su-estado-y-la-cobertura-por-fuente-sobre-la-api-p
pills: []
files:
- surface/src/workbench/SourceAnchoringView.tsx
- surface/src/workbench/anchoring-coverage.ts
- surface/src/core/similarity.ts
- surface/src/core/client.ts
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW4b: surface ancla de verdad por las rutas de sldb serve, borra el cálculo local de anclajes y muestra changed como alerta

## Rationale

_Explain why this task exists or the business driver behind it._

workbench/SourceAnchoringView.tsx crea el átomo sin offsets y recalcula el estado con indexOf; anchoring-coverage.ts arma la cobertura localmente; el umbral de duplicado es 0.85 (core/similarity.ts) y §6 dice 75 %; los parecidos salen como texto y no como enlace; el mensaje de nuevo sale sin porcentaje; y changed se muestra como ficha neutra solo en la vista 03 (§4, §6 Flujo 3). Depende de SW4a. Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233813-suggestion-sw4-flujo-3-6-4-anclar-de-verdad-hoy-crear-atomdoc-y-anclar-no-guarda-un-anclaje-y-el-estado-del-anclaje-se-calcula-en-la-ui.md.

## Goal

_Describe the concrete result this task must produce._

Crear un átomo desde una selección guarda su anclaje con offsets por sldb serve; el estado y la cobertura se leen de sldb (sin indexOf en surface); el umbral es 75 %, los parecidos enlazan al átomo y el mensaje muestra el porcentaje; changed se muestra como alerta (no error, no bloquea) en la ficha, en la lente Fierros y en el panel de cobertura, también al editar un átomo transcluido.

## Scope

_State what is in scope and what is out of scope._

Entra: SourceAnchoringView.tsx, anchoring-coverage.ts, core/similarity.ts, core/client.ts y ProsaWorkbenchView.tsx; borrar el cálculo local; tests de vista contra el cliente inyectable. No entra: rutas de sldb (SW4a).

Precisión de JP (2026-11-17, prevalece sobre lo anterior): el Workbench de sldb/surface es LA UI de SLDB, general y autónoma para cualquier store SLDB; no es una superficie de la UI de deskops. La §2 del manual (que lo presenta como superficie de deskops) está desactualizada y no es premisa de este contrato. Principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Nada del Workbench depende de que exista un desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer las rutas de SW4a. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; grep de indexOf en el cálculo de anclajes de surface no da nada; commit.

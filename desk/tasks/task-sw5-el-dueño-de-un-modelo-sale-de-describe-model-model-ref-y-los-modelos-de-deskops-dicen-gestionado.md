---
sldb:
  by: agent
  at: '2026-11-17T04:12:09Z'
  authority: generated
  via: save_document_payload
id: task-sw5-el-dueño-de-un-modelo-sale-de-describe-model-model-ref-y-los-modelos-de-deskops-dicen-gestionado
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
- desk/inbox/20261116-233840-suggestion-sw5-autoridad-por-modelo-4-el-due-o-del-modelo-sale-de-describe-model-y-los-modelos-de-deskops-muestran-el-verbo.md
depends_on:
- task-sw3-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-el-árbol-enfoca-en-vez-de-navegar-y-l
pills: []
files:
- surface/src/core/authority.ts
- surface/src/workbench/ProsaWorkbenchView.tsx
- surface/src/workbench/ModelStudioView.tsx
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW5: quién puede editar cada documento sale de lo que entrega sldb (describe_model), sin listas de modelos en la UI; 'gestionado por deskops' es un caso particular

## Rationale

_Explain why this task exists or the business driver behind it._

core/authority.ts decide qué modelos son de deskops con una lista fija de nombres y prefijos de model_ref; 'gestionado por deskops' y el verbo sugerido se calculan pero no se dibujan; y Model Studio usa otra regla (canEditModelContract) (§4). Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233840-suggestion-sw5-autoridad-por-modelo-4-el-due-o-del-modelo-sale-de-describe-model-y-los-modelos-de-deskops-muestran-el-verbo.md.

## Goal

_Describe the concrete result this task must produce._

La UI decide si un campo es editable solo con lo que entrega sldb (autoridad y model_ref de describe_model), en un solo lugar y sin listas de nombres de modelos; cuando sldb dice que un modelo lo gestiona otro sistema (por ejemplo deskops), el campo se ve de solo lectura con el texto y el verbo que sldb o el modelo declaren; Model Studio usa la misma fuente.

## Scope

_State what is in scope and what is out of scope._

Entra: core/authority.ts, ProsaWorkbenchView.tsx y ModelStudioView.tsx; confirmar si model_ref alcanza para modelos builtin de sldb, de deskops, del store local y las especializaciones de un desk; si no alcanza, nota a sldb y no ampliar la lista; tests de authority con model_ref reales del store del repo (TaskDoc, PillDoc, un modelo local y uno builtin de sldb) y un test de vista que encuentra el texto y el verbo en un campo de TaskDoc. No entra: ejecutar el verbo (SW6).

Precisión de JP (2026-11-17, prevalece sobre lo anterior): el Workbench de sldb/surface es LA UI de SLDB, general y autónoma para cualquier store SLDB; no es una superficie de la UI de deskops. La §2 del manual (que lo presenta como superficie de deskops) está desactualizada y no es premisa de este contrato. Principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Nada del Workbench depende de que exista un desk.

Decisión abierta (JP no la marcó como compromiso): si la autoridad se define por modelo. Esta tarea implementa la regla general con lo que sldb entrega hoy; si para un caso hace falta un dato que sldb no da, se manda nota a sldb y el caso queda de solo lectura con el motivo, sin inventar una regla en la UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer authority.ts y src/sldb/api/model_registry/model_description.py. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; no queda la lista fija de nombres de modelos de deskops; commit.

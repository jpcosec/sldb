---
sldb:
  by: agent
  at: '2026-11-17T02:51:56Z'
  authority: generated
  via: create_document
id: task-sw7-model-studio-edita-campos-existentes-crea-modelos-deja-que-sldb-compruebe-los-slots-de-la-planti
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
- desk/inbox/20261116-233931-suggestion-sw7-flujo-4-6-4-studio-model-studio-edita-campos-existentes-crea-modelos-y-confirma-antes-de-promover.md
depends_on: []
pills: []
files:
- surface/src/workbench/ModelStudioView.tsx
- surface/src/workbench/model-studio-logic.ts
- surface/src/core/client.ts
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW7: Model Studio edita campos existentes, crea modelos, deja que sldb compruebe los slots de la plantilla y confirma el plan antes de promover

## Rationale

_Explain why this task exists or the business driver behind it._

En workbench/ModelStudioView.tsx la tabla de FieldDecl solo agrega y quita campos, el selector de tipos es una lista fija (model-studio-logic.ts) sin DocRef[SpecDoc] ni list[DocRef], '+ Nuevo Modelo' está deshabilitado aunque sldb serve expone POST /models/create, la comprobación de slots de __template__ no se hace, promover aplica al primer clic y ⌘↵ no guarda la plantilla (§4, §6 Flujo 4, §7). Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233931-suggestion-sw7-flujo-4-6-4-studio-model-studio-edita-campos-existentes-crea-modelos-y-confirma-antes-de-promover.md.

## Goal

_Describe the concrete result this task must produce._

Model Studio edita tipo y descripción de un campo existente, ofrece los tipos que pide §6, crea modelos por POST /models/create, muestra la comprobación de slots que devuelve sldb (POST /models/validate) sin parsear la plantilla en la UI, pide confirmación con el plan de backfill antes de promover y guarda la plantilla con ⌘↵.

## Scope

_State what is in scope and what is out of scope._

Entra: ModelStudioView.tsx, model-studio-logic.ts y core/client.ts (método para POST /models/create) en surface/src; quitar el parseo local de marcadores si duplica a sldb; si sldb no devuelve la comprobación de slots, mandar nota a sldb y dejar el control deshabilitado con el motivo; tests de vista contra el cliente inyectable (sin mocks de módulo, como exige check-layers). Los modelos builtin de sldb y deskops siguen en solo lectura. No entra: archivos de SW2 a SW6.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer ModelStudioView.tsx, model-studio-logic.ts, core/client.ts y src/sldb/cli/serve/models_routes.py. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con tests de vista para editar un campo, crear un modelo, promover con confirmación y guardar con ⌘↵; commit.

---
sldb:
  by: agent
  at: '2026-11-17T04:17:28Z'
  authority: generated
  via: save_document_payload
id: task-sw9-aceptación-del-workbench-sobre-el-desk-real-vistas-flujos-atajos-colores-y-enlace-desde-deskops
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
- desk/inbox/20261116-234023-suggestion-sw9-aceptaci-n-sobre-el-desk-real-2-4-y-capturas-para-el-repaso-de-ui-con-jp.md
depends_on:
- task-sw1-documentación-y-arranque-de-surface-al-día-con-el-workbench-readme-maqueta-histórica-tareas-t7-t
- task-sw2-la-edición-en-el-lugar-confirma-con-enter-o-falla-cerrada-sin-autoridad-conocida-y-muestra-la-op
- task-sw3-las-referencias-abren-la-vista-que-corresponde-a-su-modelo-el-árbol-enfoca-en-vez-de-navegar-y-l
- task-sw4b-surface-ancla-de-verdad-por-las-rutas-de-sldb-serve-borra-el-cálculo-local-de-anclajes-y-muestr
- task-sw5-el-dueño-de-un-modelo-sale-de-describe-model-model-ref-y-los-modelos-de-deskops-dicen-gestionado
- task-sw7-model-studio-edita-campos-existentes-crea-modelos-deja-que-sldb-compruebe-los-slots-de-la-planti
pills: []
files:
- surface/package.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW9: aceptación del Workbench sobre el desk real (vistas, flujos, atajos, colores y enlace desde deskops) con capturas para el repaso de UI con JP

## Rationale

_Explain why this task exists or the business driver behind it._

JP va a repasar la UI y necesita una matriz de aceptación con capturas sobre el desk real después de SW1 a SW7. Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-234023-suggestion-sw9-aceptaci-n-sobre-el-desk-real-2-4-y-capturas-para-el-repaso-de-ui-con-jp.md.

## Goal

_Describe the concrete result this task must produce._

En runs/ queda un índice con la matriz vista x flujo (PASA o FALLA con severidad), tiempos y capturas por vista y lente sobre stores SLDB reales (el del repo sirve) y no solo sobre un desk; las fallas nuevas quedan como notas a este desk.

## Scope

_State what is in scope and what is out of scope._

Entra: los cinco puntos de la nota (vistas con lentes y tiempos; los cuatro flujos de §6 escribiendo solo en una copia del store en /dev/shm; atajos de §7; colores de papel contra src/styles/paper-tokens.css y los hex a mano; enlace desde la UI de deskops con un id real y con uno inexistente, que debe reportarse como falla si cae en silencio), con playwright y chromium sin interfaz, sldb serve sobre el store real y surface en 5174. No entra: arreglar fallas (van como notas).

Precisión de JP (2026-11-17, prevalece sobre lo anterior): el Workbench de sldb/surface es LA UI de SLDB, general y autónoma para cualquier store SLDB; no es una superficie de la UI de deskops. La §2 del manual (que lo presenta como superficie de deskops) está desactualizada y no es premisa de este contrato. Principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Nada del Workbench depende de que exista un desk.

El punto 5 (enlace desde la UI de deskops) es opcional: se prueba solo si la UI de deskops está disponible y no es criterio de aceptación de la UI de SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copia del store en /dev/shm. 2) Servidores. 3) Scripts de playwright. 4) Índice, capturas y notas. 5) Apagar todo.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

El run-dir tiene el índice completo, las capturas y los tiempos; las fallas están como notas en el inbox; no se escribió en el desk real.

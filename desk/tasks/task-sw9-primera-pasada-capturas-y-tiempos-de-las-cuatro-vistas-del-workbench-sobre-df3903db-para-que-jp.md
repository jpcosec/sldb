---
sldb:
  by: agent
  at: '2026-11-17T02:51:06Z'
  authority: generated
  via: create_document
id: task-sw9-primera-pasada-capturas-y-tiempos-de-las-cuatro-vistas-del-workbench-sobre-df3903db-para-que-jp
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
depends_on: []
pills: []
files:
- surface/package.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW9, primera pasada: capturas y tiempos de las cuatro vistas del Workbench sobre df3903db, para que JP vea el punto de partida

## Rationale

_Explain why this task exists or the business driver behind it._

JP quiere ver el estado de partida del Workbench antes de los arreglos de la serie SW. Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-234023-suggestion-sw9-aceptaci-n-sobre-el-desk-real-2-4-y-capturas-para-el-repaso-de-ui-con-jp.md.

## Goal

_Describe the concrete result this task must produce._

En runs/ queda un índice con capturas y tiempos de las cuatro vistas (#/workbench, #/diagram, #/source, #/studio), con las lentes lectura y fierros, sobre documentos reales del store del repo, tomadas en df3903db.

## Scope

_State what is in scope and what is out of scope._

Entra: solo el punto 1 de SW9: levantar sldb serve sobre una copia del store del repo en /dev/shm y surface en el puerto que use la configuración de df3903db; con playwright y chromium sin interfaz, abrir cada vista y lente sobre documentos reales, medir el tiempo de carga y de cada llamada /sldb (incluida la carga inicial de /graph completo) y sacar una captura por vista y lente. No entra: los flujos, los atajos, los colores ni el enlace desde deskops (son de SW9 completa); arreglar nada; escribir en el desk real.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copia del store en /dev/shm. 2) Levantar sldb serve y surface. 3) Script de playwright en el run-dir. 4) Índice con tabla vista x lente -> tiempo y captura. 5) Apagar los servidores y borrar la copia.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

El run-dir tiene el índice, las capturas con nombre por vista y lente y los tiempos; los servidores quedan apagados; no se escribió en el desk real.

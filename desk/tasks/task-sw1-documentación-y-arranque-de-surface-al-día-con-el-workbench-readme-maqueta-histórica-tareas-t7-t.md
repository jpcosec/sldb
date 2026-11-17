---
sldb:
  by: agent
  at: '2026-11-17T04:10:31Z'
  authority: generated
  via: save_document_payload
id: task-sw1-documentación-y-arranque-de-surface-al-día-con-el-workbench-readme-maqueta-histórica-tareas-t7-t
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
- desk/inbox/20261116-233646-suggestion-sw1-documentaci-n-y-arranque-de-surface-al-d-a-con-el-workbench.md
depends_on: []
pills: []
files:
- surface/vite.config.ts
- docs/surface/tasks/README.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW1: documentación y arranque de surface como la UI de SLDB (README, maqueta histórica, tareas T7-T9 y puerto configurable documentado)

## Rationale

_Explain why this task exists or the business driver behind it._

La UI de deskops enlaza a http://127.0.0.1:5174/#/workbench?doc=TaskDoc:<id>&lens=fierros, pero vite arranca en 5173 salvo que esté ocupado, y la documentación de surface describe la superficie anterior. Base: el rediseño del Workbench, df3903db en origin/main de sldb (JP levantó para la serie SW la restricción de no tocar surface). Especificación: docs/ui-workbench/MANUAL_DE_USUARIO_Y_ESPECIFICACION_UI.md (§n) y maquetas en docs/ui-workbench/screens/. La evidencia de la nota viene de una lectura estática: confirmar cada línea contra el código; si no calza, manda el código y se anota en result-summary.md. La UI se verifica sin interfaz con playwright y chromium en robocop2. Origen: desk/inbox/20261116-233646-suggestion-sw1-documentaci-n-y-arranque-de-surface-al-d-a-con-el-workbench.md.

## Goal

_Describe the concrete result this task must produce._

surface tiene un README que la presenta como la UI de SLDB para cualquier store y describe cómo levantarla; las referencias a la maqueta están corregidas o marcadas como históricas; docs/surface/tasks/README.md dice el estado real de T7, T8 y T9; el puerto de vite es configurable (variable de entorno, con un valor por defecto) y está documentado, sin strictPort.

## Scope

_State what is in scope and what is out of scope._

Entra: README de surface (cuatro vistas, lentes, #/legacy, proxies /sldb y /desk, contrato de capas, cómo levantarla contra un sldb serve real y contra el store demo de scripts/setup_workbench_demo_store.py); corregir o marcar como históricas las referencias a la maqueta; actualizar docs/surface/tasks/README.md; puerto configurable por variable de entorno en surface/vite.config.ts, sin strictPort, documentado (en robocop2 se usa 5174; en la máquina de JP ese puerto lo ocupa otro proyecto). No entra: cambios de comportamiento fuera del puerto.

Precisión de JP (2026-11-17, prevalece sobre lo anterior): el Workbench de sldb/surface es LA UI de SLDB, general y autónoma para cualquier store SLDB; no es una superficie de la UI de deskops. La §2 del manual (que lo presenta como superficie de deskops) está desactualizada y no es premisa de este contrato. Principios firmes: papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula. Nada del Workbench depende de que exista un desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer surface/ (README actual, vite.config.ts, src/app, src/workbench) y docs/surface/tasks/README.md. 2) Escribir y corregir la doc. 3) Puerto. 4) Levantar surface contra el store demo y comprobar que sirve en 5174. 5) Validation.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; con la variable de entorno del puerto, npm run dev sirve en ese puerto y sin ella en el valor por defecto documentado; el README presenta la UI de SLDB y cómo levantarla contra un sldb serve real y contra el store demo; commit.

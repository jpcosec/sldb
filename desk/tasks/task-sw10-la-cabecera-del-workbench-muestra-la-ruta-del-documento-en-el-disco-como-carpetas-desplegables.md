---
sldb:
  by: agent
  at: '2026-11-17T05:11:20Z'
  authority: generated
  via: create_document
id: task-sw10-la-cabecera-del-workbench-muestra-la-ruta-del-documento-en-el-disco-como-carpetas-desplegables
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
- desk/inbox/20261117-011458-suggestion-sw10-cabecera-del-workbench-la-ruta-del-documento-debe-ser-un-navegador-de-disco.md
depends_on: []
pills: []
files:
- surface/src/app/WorkbenchShell.tsx
- surface/src/styles/paper-tokens.css
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SW10: la cabecera del Workbench muestra la ruta del documento en el disco como carpetas desplegables navegables

## Rationale

_Explain why this task exists or the business driver behind it._

JP pidió (comentario sobre la interfaz, 2026-11-17) que la cabecera muestre dónde está el archivo en el disco y deje moverse por carpetas y archivos desde ahí, en vez de modelo e id; aceptó en vivo la variante de carpetas desplegables con la ruta completa. Cada documento de GET /graph ya trae su path relativo al store. Origen: desk/inbox/20261117-011458-suggestion-sw10-cabecera-del-workbench-la-ruta-del-documento-debe-ser-un-navegador-de-disco.md.

## Goal

_Describe the concrete result this task must produce._

La cabecera muestra la ruta real del documento abierto: la raíz del store y cada carpeta son segmentos que abren un panel con sus subcarpetas (con la cantidad de documentos) y sus documentos; un clic abre el documento; el nombre del archivo al final abre ⌘K; funciona con teclado y mouse y una ruta de 150 caracteres no desborda la cabecera a 1280 px.

## Scope

_State what is in scope and what is out of scope._

Entra: la cabecera en surface/src/app/WorkbenchShell.tsx y sus estilos (paper-tokens.css), agrupando por path solo lo que sldb entrega en /graph (la UI no recorre el disco); las vistas sin documento (Model Studio) muestran la raíz del store; tests de vitest del listado por carpeta y de la navegación, actualizando los que usan breadcrumb-doc-switch y wb-context-pill. Si se quiere mostrar Markdown sin modelo o carpetas sin documentos, falta una operación de sldb que liste el árbol del store: se pide por nota a sldb y queda fuera de esta tarea. Precisión de JP: el Workbench es la UI de SLDB, general para cualquier store; papel con fierros ocultables, toda escritura tiene nombre, la UI no calcula.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer WorkbenchShell.tsx, core/contract.ts (GraphDocument.path) y los tests de la cabecera. 2) Implementar. 3) Tests. 4) Validation y verificación con playwright sobre un store real.

## Validation

_List the checks required before this task can close._

- cd surface && npm test
- cd surface && npx tsc -b --noEmit

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; una captura de playwright a 1280 px con una ruta larga queda en el run-dir; commit.

FILE:desk/tasks/task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer.md
---
sldb:
  by: agent
  at: '2026-11-23T17:38:15Z'
  authority: generated
  via: save_document_payload
id: task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-142617-suggestion-traer-a-surface-el-lector-de-documentos-de-minegocio-para-explorar-deskops.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# surface trae el lector de documentos de minegocio (indice por carpeta o semantica, lectura, ficha, referencias, rechazos legibles) para explorar el store de deskops

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-142617-suggestion-traer-a-surface-el-lector-de-documentos-de-minegocio-para-explorar-deskops (JP 2026-11-23): JP quiere explorar el store de deskops con el lector que quedo en la copia de surface de minegocio (commit ab8fac2, partio de sldb 562847e2). Fuente copiada en /mnt/ssd/proyectos/SLDB_1/reports/lector-minegocio-20261123/superficie.

## Goal

_Describe the concrete result this task must produce._

sldb/surface tiene la parte generica del lector de minegocio: indice por carpeta o por semantica, lectura de un documento, ficha, referencias entre documentos y rechazos legibles; funciona contra sldb serve sobre el store real de deskops; lo especifico del negocio queda fuera.

## Scope

_State what is in scope and what is out of scope._

Entra: portar a surface src/core/{doc-ref,wiki-index,rechazo,imagenes}.ts con sus tests y la fixture rechazos-sldb.json, src/workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx y WikiLectura.test, y los cambios genericos en core/client.ts, core/layout.ts, main.tsx, react/{context,DocumentSurface,useDocumentEditor}, paper-tokens.css, ComposerView, ProsaWorkbenchView, workbench.test. Ojo: WorkbenchShell.tsx, vite.config.ts y tsconfig son trabajo local de JP: no se tocan sin dejarlo explicito en el informe para que el coordinador avise antes de integrar. Fuera: textos, rutas y datos del negocio de minegocio. El agrupado por semantica depende de que deskops unifique sus tags (deskops task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig); si no esta, agrupar por carpeta y dejar la semantica conectada.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) diff de reports/lector-minegocio-20261123/superficie contra surface/ para separar generico de especifico. 2) Portar core y sus tests. 3) Portar workbench y react. 4) tsc, vitest y check-layers. 5) Levantar sldb serve sobre el store de deskops y medir el tiempo de carga de cada pantalla (indice, lectura, ficha).

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run && el script check-layers del package.json

## Done When

_Name the observable condition that makes the task complete._

tsc, vitest y check-layers de surface pasan; el informe trae la lista de archivos portados y los dejados fuera con motivo, y los tiempos medidos de cada pantalla contra el store de deskops; WorkbenchShell.tsx, vite.config.ts y tsconfig sin cambios o con el cambio senalado.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


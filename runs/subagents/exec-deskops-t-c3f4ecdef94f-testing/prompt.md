Task: task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer
Title: surface trae el lector de documentos de minegocio (indice por carpeta o semantica, lectura, ficha, referencias, rechazos legibles) para explorar el store de deskops
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-23T18:16:08Z'
  authority: generated
  via: save_document_payload
id: task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261123-142617-suggestion-traer-a-surface-el-lector-de-documentos-de-minegocio-para-explorar-deskops.md
- desk/inbox/20261121-210430-unclear-la-superficie-trata-todo-field-como-bloque-porque-el-servidor-manda-composition-null.md
- desk/inbox/20261121-213216-unclear-la-superficie-no-puede-saber-la-ruta-ni-la-cardinalidad-de-un-modelo-al-crear-un-documento.md
- desk/inbox/20261121-220138-unclear-sldb-serve-no-deja-leer-ni-reparar-nada-cuando-un-documento-del-store-es-invalido.md
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-surface-trae-el-lector-de-documentos-de-minegocio-indice-por-carpeta-o-semantica-lectura-ficha-refer"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-c3f4ecdef94f"

## Gates rapidos del desk

Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Si termina con rc distinto de 0 el veredicto es FALLA.

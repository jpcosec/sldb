Task: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa
Title: El lector de surface queda sin residuos de minegocio: businessName, NegocioDoc y textos del negocio salen de wiki-index y sus tests
Status: draft
Current node: ritual-execution
Task type: task.refactor
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-refactor] TaskRefactorDoc:task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa: Una tarea task.refactor se activa, además de lo que pide task.code, con un recibo goldens aceptado e intacto. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "goldens") (seen: {}) (witness: ReviewDoc:review-task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T13:08:20Z'
  authority: generated
  via: save_document_payload
id: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El lector de surface queda sin residuos de minegocio: businessName, NegocioDoc y textos del negocio salen de wiki-index y sus tests

## Rationale

_Explain why this task exists or the business driver behind it._

Al cerrar task-surface-trae-el-lector-de-documentos-de-minegocio-... (3cc5c36b) el tester encontro residuos especificos de minegocio en codigo de produccion (businessName, NegocioDoc, 'La wiki de tu negocio', 'Este negocio ya tiene su pagina') en surface/src/core/wiki-index.ts y sus tests; el alcance pedia dejarlos fuera. Son inertes en deskops pero ensucian el lector generico.

## Goal

_Describe the concrete result this task must produce._

surface/src no nombra NegocioDoc, businessName ni textos del negocio (fuera de WorkbenchShell.tsx, que no se toca). El titulo del indice de wiki-index sale del nombre del store (el ultimo segmento de la ruta del store que surface ya conoce); si no hay, el texto fijo 'Documentos'. tsc, vitest y check-layers pasan.

## Scope

_State what is in scope and what is out of scope._

surface/src entero salvo vite.config.ts y tsconfig. Por decision de JP (2026-11-25) entran tambien src/app/WorkbenchShell.tsx y src/app/workbench.test.tsx. Ademas de lo del intento 2 (core/wiki-index.ts y su test, WikiLectura.test.tsx, core/imagenes.ts, core/rechazo.ts con test y fixture rechazos-sldb.json, core/doc-ref.test.ts, textos de styles/paper-tokens.css).

## Implementation Path

_Outline the expected implementation route or affected surface._

Intento 3. Partir del trabajo del intento 2: en tu worktree, git cherry-pick ef45950d (rama deskops/deskops-e-b6060046cf05: storeTitle, DocumentoDoc, textos) y seguir. Decision de JP: businessName y el caso NegocioDoc se BORRAN, sin alias: (1) quitar businessName de core/wiki-index.ts (y el alias que dejo el intento 2); (2) en src/app/WorkbenchShell.tsx quitar el import de businessName (l.6) y el bloque de l.174-180 (negocio, esWiki por NegocioDoc, document.title = negocio, y el texto wiki-business-name de l.~349); el modo de lectura sin maquinaria queda generico: wikiLectura = route.view === 'workbench' && route.lens === 'lectura' para cualquier store, y la barra y document.title muestran storeTitle(ruta del store) en ese modo; (3) l.109 y l.168 eligen el documento inicial buscando un modelo que contenga 'informe' (resto del demo Levira): pasan a route.doc si viene, si no documents[0] (items?.[0] en l.109); (4) en src/app/workbench.test.tsx borrar el test de l.~387 'wiki de un negocio en Lectura...' (espera Peluqueria Rayen) y ajustar el que espera 'InformeDoc' como documento inicial (l.~384) al nuevo criterio (primer documento); si hace falta, un test nuevo de que en Lectura se ve storeTitle. 5) cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app src/workbench && node scripts/check-layers.mjs.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app src/workbench && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rniE 'NegocioDoc|businessName|negocio' surface/src no devuelve nada; grep -n 'informe' surface/src/app/WorkbenchShell.tsx no devuelve nada; tsc, los vitest de src/core src/react src/views src/app src/workbench y check-layers pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-0c6728c9fc59"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-0c6728c9fc59`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-0c6728c9fc59

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

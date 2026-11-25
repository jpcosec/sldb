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
  at: '2026-11-25T06:23:09Z'
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

surface/src entero salvo WorkbenchShell.tsx, app/workbench.test.tsx, vite.config.ts y tsconfig (no se tocan: WorkbenchShell es trabajo local de JP). Entran: core/wiki-index.ts y su test, WikiLectura.test.tsx, core/imagenes.ts, core/rechazo.ts con su test y la fixture rechazos-sldb.json, core/doc-ref.test.ts, los textos de styles/paper-tokens.css y cualquier otra fixture que nombre NegocioDoc o businessName.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep -rniE 'NegocioDoc|businessName|negocio' surface/src --exclude=WorkbenchShell.tsx --exclude=workbench.test.tsx para el inventario. 2) En core/wiki-index.ts la funcion generica se llama storeTitle (titulo = ultimo segmento de la ruta del store o 'Documentos'); WorkbenchShell.tsx importa businessName de ese modulo y no se toca, asi que wiki-index exporta ademas, en una sola linea, el alias deprecado 'export const businessName = storeTitle' con un comentario '// alias para WorkbenchShell.tsx (trabajo local de JP); se borra cuando el shell migre a storeTitle'. Nada mas usa businessName. 3) Mensajes con 'negocio' pasan a 'documento' o 'pagina'; tipos NegocioDoc pasan a un nombre generico (p. ej. DocumentoDoc) salvo donde WorkbenchShell lo importe, en cuyo caso queda el mismo patron de alias deprecado de una linea. 4) Ajustar tests y fixtures. 5) cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app && node scripts/check-layers.mjs.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rniE 'NegocioDoc|businessName|negocio' surface/src --exclude=WorkbenchShell.tsx --exclude=workbench.test.tsx solo devuelve las lineas de alias deprecado marcadas con el comentario de WorkbenchShell; tsc, los vitest de src/core src/react src/views src/app y check-layers pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-b6060046cf05"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-b6060046cf05`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-b6060046cf05

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

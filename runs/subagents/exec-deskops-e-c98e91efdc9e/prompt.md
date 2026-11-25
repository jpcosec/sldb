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
  at: '2026-11-25T03:46:51Z'
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

surface/src entero salvo WorkbenchShell.tsx, vite.config.ts y tsconfig (no se tocan): en la practica core/wiki-index.ts, wiki-index.test.ts, WikiLectura.test.tsx y la fixture que nombre NegocioDoc o businessName (encontrarla con el grep del paso 1).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep -rniE 'NegocioDoc|businessName|negocio' surface/src --exclude=WorkbenchShell.tsx para el inventario completo (incluye 'Este negocio ya tiene su pagina' y 'tu negocio'). 2) Reemplazar cada uno: titulo = nombre del store o 'Documentos'; mensajes con 'negocio' pasan a 'documento' o 'pagina'. 3) Ajustar tests y fixture. 4) cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views && node scripts/check-layers.mjs.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rniE 'NegocioDoc|businessName|negocio' surface/src --exclude=WorkbenchShell.tsx no devuelve nada; tsc, los vitest de esos directorios y check-layers pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-c98e91efdc9e"

## Gates rapidos del desk

Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):

    bash tools/check.sh --fast

Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. Anota el comando y su rc en validation.log.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-c98e91efdc9e`:

    /mnt/ssd/proyectos/SLDB_1/sldb/.worktrees/deskops-e-c98e91efdc9e

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/sldb. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/sldb`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

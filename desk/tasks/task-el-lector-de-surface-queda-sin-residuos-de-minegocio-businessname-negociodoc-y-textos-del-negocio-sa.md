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

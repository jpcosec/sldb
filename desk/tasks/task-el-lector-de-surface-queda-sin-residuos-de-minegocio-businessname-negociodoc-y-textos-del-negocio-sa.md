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

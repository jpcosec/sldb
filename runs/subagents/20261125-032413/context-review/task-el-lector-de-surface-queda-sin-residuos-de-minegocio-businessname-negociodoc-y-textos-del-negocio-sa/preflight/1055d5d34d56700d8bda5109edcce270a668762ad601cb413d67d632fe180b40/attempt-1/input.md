FILE:desk/tasks/task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa.md
---
sldb:
  by: agent
  at: '2026-11-24T02:22:22Z'
  authority: generated
  via: create_document
id: task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

surface/src/core/wiki-index.ts y sus tests no nombran NegocioDoc, businessName ni textos del negocio; el titulo del indice sale de un dato generico (nombre del store o del documento raiz) con un texto de respaldo neutro; tsc, vitest y check-layers pasan.

## Scope

_State what is in scope and what is out of scope._

surface/src/core/wiki-index.ts, wiki-index.test.ts, WikiLectura.test.tsx y la fixture que lo necesite. No tocar WorkbenchShell.tsx, vite.config.ts ni tsconfig.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep de NegocioDoc, businessName y 'negocio' en surface/src. 2) Reemplazar por un dato generico. 3) Ajustar tests. 4) tsc, vitest y check-layers.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rn 'NegocioDoc\|businessName\|tu negocio' surface/src (salvo WorkbenchShell.tsx, que no se toca) vacio; tsc, vitest y check-layers verdes.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


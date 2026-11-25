FILE:desk/tasks/task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura.md
---
sldb:
  by: agent
  at: '2026-11-25T14:28:06Z'
  authority: generated
  via: create_document
id: task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# surface borra el alias muerto businessName y el shell muestra el nombre real del store en Lectura

## Rationale

_Explain why this task exists or the business driver behind it._

Tester de task-el-lector-de-surface-queda-sin-residuos-de-minegocio-businessname-negociodoc-y-textos-del-negocio-sa (runs/subagents/exec-deskops-t-78c922eaaaca-testing, FALLA): el reap integro tambien la rama del intento 2 (c5a8a9dd), que reintrodujo en surface/src/core/wiki-index.ts:127-128 el alias 'export const businessName = ... => null' (codigo muerto, nadie lo importa). Ademas WorkbenchShell recibe una prop nueva storePath que ningun caller pasa (src/main.tsx:28), asi que en la app real Lectura muestra siempre 'Documentos'. Decision de JP: businessName se borra sin alias.

## Goal

_Describe the concrete result this task must produce._

Que surface/src no nombre businessName ni negocio y que la barra de Lectura muestre el nombre del store servido.

## Scope

_State what is in scope and what is out of scope._

surface/src/core/wiki-index.ts, surface/src/main.tsx y, si hace falta, el cliente de surface y un test. Fuera: sldb serve (si no expone la ruta del store, pedirlo por inbox a sldb y usar 'Documentos' mientras tanto).

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. 1) Borrar wiki-index.ts:127-128 (comentario y alias), sin sustituto. 2) main.tsx pasa storePath a WorkbenchShell: averiguar de donde lo obtiene surface hoy (cliente de sldb serve: /health, /schema u otra ruta que ya traiga la ruta o el nombre del store; ver src/sldb/cli/serve/health.py y routes.py). Si ya existe, usarla; si no, dejar 'Documentos' y mandar una nota al inbox de sldb pidiendo el nombre del store en /health. 3) Test: wiki-index.test.ts ya prueba storeTitle; agregar o ajustar un test de main/shell si se cablea storePath. No poner Task-Id en el commit de codigo.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app src/workbench && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rniE 'NegocioDoc|businessName|negocio' surface/src no devuelve nada; Lectura muestra el nombre del store si sldb serve lo expone (o hay nota a sldb pidiendolo); tsc, vitest de src/core src/app y check-layers pasan.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


---
sldb:
  by: agent
  at: '2026-11-25T18:08:31Z'
  authority: generated
  via: save_document_payload
id: task-surface-borra-el-alias-muerto-businessname-y-el-shell-muestra-el-nombre-real-del-store-en-lectura
status: ready_for_testing
summary: ''
tags: []
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- surface/src/app/WorkbenchShell.tsx
- surface/src/app/workbench.test.tsx
- surface/src/core/client.ts
- 35d35097fba74e27b26cc20c24aaf35b92df50af
- 9384682f
depends_on: []
pills: []
files:
- surface/src/app/WorkbenchShell.tsx
- surface/src/app/workbench.test.tsx
- surface/src/core/client.ts
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lectura-de-surface-muestra-el-nombre-del-store-servido-y-no-queda-alias-businessname
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

Intento 2 (tester FALLA en runs/subagents/exec-deskops-t-fcebfb9c80fb-testing): el alias ya esta borrado (9384682f), NO lo rehagas. Falta lo segundo: sldb serve SI expone la ruta del store: GET /stores devuelve {store: str(store_path), root: ...} (src/sldb/cli/serve/stores_routes.py:33-35, probado en tests/test_serve.py::test_stores_describe_current_store). Hacer que surface la pida (con el cliente de surface, src/core/client.ts, si no tiene metodo para /stores agregarlo) y que src/main.tsx pase storePath a WorkbenchShell (hoy l.28 no lo pasa), con la carga asincrona que use el resto del cliente; mientras carga o si falla, 'Documentos'. Test: un vitest del cliente o de main que, con fetch mockeado de /stores, muestre el nombre del store en Lectura. No poner Task-Id en el commit de codigo.

## Validation

_List the checks required before this task can close._

- cd surface && npx tsc --noEmit && npx vitest run src/core src/react src/views src/app src/workbench && node scripts/check-layers.mjs

## Done When

_Name the observable condition that makes the task complete._

grep -rniE 'NegocioDoc|businessName|negocio' surface/src no devuelve nada; Lectura muestra el nombre del store si sldb serve lo expone (o hay nota a sldb pidiendolo); tsc, vitest de src/core src/app y check-layers pasan.

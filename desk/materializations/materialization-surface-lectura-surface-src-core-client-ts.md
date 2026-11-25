---
sldb:
  by: agent
  at: '2026-11-25T18:10:21Z'
  authority: generated
  via: create_document
id: materialization-surface-lectura-surface-src-core-client-ts
title: surface-lectura surface-src-core-client-ts
source_atoms:
- atom-lectura-de-surface-muestra-el-nombre-del-store-servido-y-no-queda-alias-businessname
target_kind: code
target_identity: surface/src/core/client.ts
validation:
- cd surface && npx vitest run src/app/workbench.test.tsx -t Lectura
tags:
- system:sldb
- topic:surface-lectura
---

# surface-lectura surface-src-core-client-ts

## Intent

materializa en surface/src/core/client.ts el atom atom-lectura-de-surface-muestra-el-nombre-del-store-servido-y-no-queda-alias-businessname

---
sldb:
  by: agent
  at: '2026-11-21T14:25:38Z'
  authority: generated
  via: create_document
id: atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido
title: El rollback de una transacción restaura el conjunto sucio persistido
five_wh_one_plus: how
tags:
- system:sldb
- topic:store
---

# El rollback de una transacción restaura el conjunto sucio persistido

## Answer

TransactionState toma una instantánea de .sldb_cache/documents_dirty.json al entrar. Tras forget_caches lo restaura y llama a documents_dirty.reload, para que la memoria y el disco queden como antes de la transacción (4b44a43a). Arregla la regresión de 6772820a: tests/api vuelve a 0 fallas, y el coordinador verificó en worktree limpio tests/api, tests/store, código limpio y la spec del lenguaje con 2390 passed.

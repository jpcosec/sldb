---
sldb:
  by: agent
  at: '2026-11-09T17:25:11Z'
  authority: generated
  via: create_document
id: atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback
title: La transacción restaura el dirty set de reglas en el rollback
five_wh_one_plus: what
tags:
- system:sldb
- topic:transaction
---

# La transacción restaura el dirty set de reglas en el rollback

## Answer

Una transacción de sldb guarda una copia de .sldb_cache/rules/dirty.json al abrirse (TransactionState.__init__), así que el rollback lo restaura igual que los documentos; sin esa copia, un store con RuleDocs convertía cualquier rollback en RollbackError y escondía el error original (decisión s1, revisable).

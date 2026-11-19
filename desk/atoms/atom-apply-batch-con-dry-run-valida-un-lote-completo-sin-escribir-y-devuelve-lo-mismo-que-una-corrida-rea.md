---
sldb:
  by: agent
  at: '2026-11-19T04:37:48Z'
  authority: generated
  via: create_document
id: atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea
title: apply_batch con dry_run valida un lote completo sin escribir y devuelve lo
  mismo que una corrida real
five_wh_one_plus: how
tags:
- system:sldb
- topic:api
---

# apply_batch con dry_run valida un lote completo sin escribir y devuelve lo mismo que una corrida real

## Answer

sldb.api.apply_batch(store, changes, dry_run=True) corre la misma prevalidación que una corrida real (forma, modelo, round-trip, destinos y guardas de batch_guards.check_guards) bajo el mismo store_lock y vuelve antes de abrir la transacción. Un lote válido devuelve un BatchReport con dry_run=True y saved e inverse vacíos. Uno inválido levanta las mismas excepciones que la corrida real (SLDBValidationError, SLDBStoreError, ConflictError). En los dos casos no se escribe nada en el store ni en el proyecto. Es la forma de validar un lote antes de aplicarlo, como hace propose_changes del MCP.

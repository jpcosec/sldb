---
sldb:
  by: agent
  at: '2026-11-16T19:44:52Z'
  authority: generated
  via: create_document
id: atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso
title: apply_batch prevalida y escribe bajo el cerrojo del store y rechaza con ConflictError
  un guarda obsoleto
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-lock
provenance: tarea 022444, piloto scion + ejecutor deskops-e-4e4ba795934b, tester deskops-t-a6ddcc3e4afc
  PASA
---

# apply_batch prevalida y escribe bajo el cerrojo del store y rechaza con ConflictError un guarda obsoleto

## Answer

apply_batch toma store_lock(store, wait=True) alrededor de la prevalidación y de toda la transacción; update pasa expected_source_hash y expected a tx.update, y delete, move y untrack quedan protegidos porque la prevalidación corre bajo el mismo cerrojo. StoreIOLock es reentrante dentro del proceso (contador por ruta resuelta), así que una escritura anidada no se bloquea a sí misma. Dos procesos con el mismo guarda: uno escribe y el otro recibe ConflictError sin escritura parcial. La exclusión es por proceso, no por hilo.

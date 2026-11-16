---
sldb:
  by: agent
  at: '2026-11-16T10:23:20Z'
  authority: generated
  via: create_document
id: atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa
title: Un lector que no debe escribir abre el store con read_store, que no migra y
  rechaza un store no preparado
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: src/sldb/api/stores/read_store.py
---

# Un lector que no debe escribir abre el store con read_store, que no migra y rechaza un store no preparado

## Answer

sldb.api.read_store(store) resuelve el store igual que open_store pero nunca llama a migrate_store_layout. Si el layout no es canónico (store_is_prepared es False), lanza SLDBStoreError('store not prepared: run `sldb stores update`'). Si lo es, empieza una operación nueva (ve altas y bajas de otros procesos) y devuelve StoreLocation sin escribir en disco. sldb.api.extract_payload(model_type, markdown) extrae el payload de un texto ya leído. open_store sigue siendo la puerta para escribir.

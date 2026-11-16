---
sldb:
  by: agent
  at: '2026-11-16T22:50:52Z'
  authority: generated
  via: create_document
id: atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
title: track con force re-indexa desde el archivo un documento ya trackeado en la
  misma ruta
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: tarea CI2 (nota sldb-ui 162239 y job store del CI sobre c5cb52f0), ejecutor
  deskops-e-146155e482b3, tester deskops-t-eab6088c807b PASA
---

# track con force re-indexa desde el archivo un documento ya trackeado en la misma ruta

## Answer

track_document_file(..., force=True) y docs track --force saltan la comprobación de round-trip y, si el documento (modelo, nombre) ya está trackeado en la misma ruta del proyecto, lo re-indexan desde el contenido actual del archivo (shard, índice y aristas) bajo store_lock; repetirlo sin cambios es idempotente y declare_tracked no duplica la entrada. Con force y otra ruta falla con SLDBStoreError que nombra las dos rutas (para mover está move). Sin force, el error 'Doc <n> already tracked.' no cambia.

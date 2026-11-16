---
sldb:
  by: agent
  at: '2026-11-16T20:31:24Z'
  authority: generated
  via: create_document
id: atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas
title: apply_batch devuelve en BatchReport.inverse el lote que lo deshace, con guardas
five_wh_one_plus: what
tags:
- system:sldb
- topic:batch
provenance: tarea 123855 (IR04b), ejecutor deskops-e-779515b3884a, tester deskops-t-937f21dafaca
  PASA
---

# apply_batch devuelve en BatchReport.inverse el lote que lo deshace, con guardas

## Answer

Bajo el cerrojo del store, apply_batch anota el estado previo de cada cambio y, tras la transacción, arma BatchReport.inverse: create->delete, update->update con el payload previo, delete->create con modelo, ruta y payload previos, move->move de vuelta, track<->untrack; cada paso lleva expected_source_hash del estado nuevo salvo el track inverso de un untrack. Deshacer es apply_batch(report.inverse): deja payloads e índice como antes y bytes iguales en documentos canónicos (la procedencia sldb.by/at/via puede cambiar). Si alguien escribió entre medio, el inverso se rechaza con ConflictError (o SLDBStoreError si el documento fue recreado) sin escritura parcial.

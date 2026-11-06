---
id: atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada
title: Una escritura de varios documentos en sldb es todo o nada
five_wh_one_plus: what
tags:
- system:sldb
- topic:transactions
- topic:write-api
provenance: docs/architecture/transactions.md
---

# Una escritura de varios documentos en sldb es todo o nada

## Answer

Toda escritura de sldb que toca más de un documento (sldb.api.transaction, apply_batch, move_document y POST /save de sldb serve) es atómica: si un cambio falla, se restauran los bytes de los archivos, las entradas del índice y los shards (documents, semantic, sections, edges) al estado previo, y el store vuelve a pasar stores check. Las transacciones se anidan y la más externa decide. Una guarda de concurrencia vieja (expected_sha256 o expected_source_hash) es un ConflictError que no escribe nada (409 en serve). Si el rollback mismo no puede restaurar algo, levanta RollbackError con la lista de rutas sin restaurar en vez de dejar el store a medias en silencio. Toda ruta de escritura (fields update, docs update, /save, apply_batch, transaction) valida contra el modelo, y un payload que el model_validator rechaza no llega al disco (G4); por /save eso es un 422. Decisión DA2 del dueño y G4 del plan generalizar-desde-deskops; implementado en GD24.

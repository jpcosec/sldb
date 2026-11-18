---
sldb:
  by: agent
  at: '2026-11-18T23:45:14Z'
  authority: generated
  via: create_document
id: atom-undo-changes-de-sldb-mcp-restaura-el-mismo-contenido-salvo-procedencia-y-deshace-n-lotes-todo-o-nada
title: undo_changes de sldb mcp restaura el mismo contenido salvo procedencia y deshace
  N lotes todo o nada
five_wh_one_plus: how
tags:
- system:sldb
- topic:mcp
---

# undo_changes de sldb mcp restaura el mismo contenido salvo procedencia y deshace N lotes todo o nada

## Answer

Deshacer es una escritura nueva: undo_changes devuelve cada documento al contenido que tenía y re-sella su procedencia (el bloque sldb: by, at, authority, via) y los hashes derivados del índice. El inverso de cada lote lleva el guard expected_content_hash (sha256 del texto sin el bloque sldb, src/sldb/api/documents/content_hash.py) en lugar de expected_source_hash, así que un documento que otro cambió y después volvió al mismo contenido no queda stale. undo_changes(steps=N) encadena los N inversos con api.apply_batches en una sola transacción bajo el cerrojo del store, cada lote validado contra el estado que deja el anterior. Si uno se rechaza, no se escribe nada y la pila queda intacta. Los demás llamadores de apply_batch siguen con expected_source_hash.

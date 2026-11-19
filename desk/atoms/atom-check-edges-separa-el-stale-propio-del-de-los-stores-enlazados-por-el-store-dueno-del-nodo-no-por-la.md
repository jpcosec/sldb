---
sldb:
  by: agent
  at: '2026-11-19T07:16:48Z'
  authority: generated
  via: create_document
id: atom-check-edges-separa-el-stale-propio-del-de-los-stores-enlazados-por-el-store-dueno-del-nodo-no-por-la
title: check_edges separa el stale propio del de los stores enlazados por el store
  dueño del nodo, no por la forma del id
five_wh_one_plus: how
tags:
- system:sldb
- topic:edges
---

# check_edges separa el stale propio del de los stores enlazados por el store dueño del nodo, no por la forma del id

## Answer

sldb.api.check_edges (src/sldb/api/edges/check_edges.py) devuelve en stale los documentos stale de este store y en linked_stale los de sus stores enlazados, que no son un fallo aquí. La separación mira de qué store viene cada nodo en el índice federado. No cuenta los ':' del id (store:Model:nombre frente a Model:nombre), porque un nombre con ':' lo confunde en los dos sentidos.

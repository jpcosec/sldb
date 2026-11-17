---
sldb:
  by: agent
  at: '2026-11-17T14:09:07Z'
  authority: generated
  via: create_document
id: atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice
title: read_store dice store not found si el .sldb no existe y store not prepared
  si le falta el índice
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: tarea de read_store (nota de graph_ui 021515); ejecutor deskops-e-4301e4e74c7c,
  tester PASA en runs/subagents/20261116-test-rs
---

# read_store dice store not found si el .sldb no existe y store not prepared si le falta el índice

## Answer

sldb.api.read_store lanza SLDBStoreError 'store not found: <ruta .sldb resuelta>' cuando el directorio del store no existe, sin crearlo, y conserva 'store not prepared: run sldb stores update (<ruta>)' cuando el store existe pero le falta core/store_index.yaml. Así un consumidor (graph_ui) no guía al operador a correr stores update sobre un store que no está.

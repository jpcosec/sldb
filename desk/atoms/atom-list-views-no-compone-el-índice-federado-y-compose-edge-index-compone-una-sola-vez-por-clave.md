---
sldb:
  by: agent
  at: '2026-11-16T20:11:51Z'
  authority: generated
  via: create_document
id: atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave
title: list_views no compone el índice federado y compose_edge_index compone una sola
  vez por clave
five_wh_one_plus: what
tags:
- system:sldb
- topic:serve
provenance: tarea de la fuga de sldb serve (nota de graph_ui 20261116-101851), ejecutor
  deskops-e-0d2adfe5edff, tester deskops-t-8fa6a308e8be PASA
---

# list_views no compone el índice federado y compose_edge_index compone una sola vez por clave

## Answer

list_views lista las vistas locales y de los stores enlazados (federación transitiva) leyendo solo los shards de aristas del modelo ViewDoc de cada store (view_nodes), sin llamar a compose_edge_index. compose_edge_index guarda un lock por clave (compose_lock): N peticiones concurrentes en frío con la misma clave componen una sola vez, y claves distintas componen en paralelo. En el caso mínimo de graph_ui el RSS de sldb serve bajó de 2,24 GB a 104 MB.

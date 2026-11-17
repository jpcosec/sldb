---
sldb:
  by: agent
  at: '2026-11-17T15:45:06Z'
  authority: generated
  via: create_document
id: atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e
title: Toda función pública de escritura de sldb.api que recibe actor lo lleva al
  sello sldb.by o declara en su docstring que no se registra
five_wh_one_plus: what
tags:
- system:sldb
- topic:provenance
provenance: tarea del parámetro actor (análisis del supervisor); ejecutor deskops-e-13131c57ccbe,
  tester PASA en runs/subagents/20261116-test-actor
---

# Toda función pública de escritura de sldb.api que recibe actor lo lleva al sello sldb.by o declara en su docstring que no se registra

## Answer

En sldb.api, una función pública de escritura con parámetro actor lo propaga hasta stamped/stamped_file, así que un documento escrito con actor=X queda con sldb.by = X; con actor=None manda el actor del proceso (set_actor, SLDB_ACTOR o agent). write_anchor y record_reconnection lo hacen desde 2026-11-17. Las escrituras que no producen un documento firmado (track/untrack, operaciones de modelo, delete_document, escrituras del DAG semántico) lo aceptan por compatibilidad y lo dicen en su docstring: no se registra.

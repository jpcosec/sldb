---
sldb:
  by: agent
  at: '2026-11-16T20:56:59Z'
  authority: generated
  via: create_document
id: atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia
title: graph_path con explain devuelve por cada tramo las aristas que lo justifican
  y su procedencia
five_wh_one_plus: what
tags:
- system:sldb
- topic:graph
provenance: tarea B3 (IR10), ejecutor deskops-e-884be32362ef, tester deskops-t-b4736317f0b4
  PASA
---

# graph_path con explain devuelve por cada tramo las aristas que lo justifican y su procedencia

## Answer

graph_path(..., explain=True) devuelve {path, steps}; graph_paths una lista de esos. Cada step es un par consecutivo {source, target, edges}; cada arista lleva relation, direction (forward|backward) y provenance {origin, relation_doc si origin es relation_doc, field si es schema, from_store si viene de un store enlazado}, sin claves vacías ni evidence. Orden: relation_doc > schema > structural > alias, desconocidos al final, empates por relation y luego relation_doc o field. Una arista espejo aparece como su directa en backward. Sin explain la forma no cambia. Expuesto como sldb graph path --explain y GET /graph/path?explain=1.

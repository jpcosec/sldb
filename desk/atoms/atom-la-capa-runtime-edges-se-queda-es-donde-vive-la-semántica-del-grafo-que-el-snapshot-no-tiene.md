---
id: atom-la-capa-runtime-edges-se-queda-es-donde-vive-la-semántica-del-grafo-que-el-snapshot-no-tiene
title: 'La capa runtime/edges se queda: es donde vive la semántica del grafo que el
  snapshot no tiene'
five_wh_one_plus: why
tags:
- system:sldb
- topic:graph
- topic:architecture
provenance: docs/architecture/edges-retirement-plan.md
---

# La capa runtime/edges se queda: es donde vive la semántica del grafo que el snapshot no tiene

## Answer

El retiro de runtime/edges (docs/architecture/edges-retirement-plan.md) se canceló el 2026-10-18. La capa siguió creciendo después del plan: referencias declaradas por id sin calificar y por path con unresolved_references, modelos heredados de un store enlazado (links_to, origin_store, has_model many_to_many), chequeo de aristas federado que separa lo propio de lo enlazado, y shards que siguen al contrato del modelo. El snapshot de src/sldb/store/graph se genera desde esos shards; retirarlos exigiría portar todo eso (gaps G1-G6, con G3 y G5 ya más grandes que en el plan).

---
layer: store
id: graph-store
title: Graph store
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-graph
provenance: source docs/core/reasoning.md
---

# Graph store

## Answer

The graph store is the persistent kernel repository for canonical documents, nodes, edges, revisions, and transaction lineage.

## Supporting points

- Its sources of truth are the transaction log, revision store, content-addressed store, and per-document heads.
- Petgraph, indexes, embeddings, caches, and semantic projections are rebuildable materializations, not primary persistence.
- The store must preserve the distinction between structural ownership edges and non-structural reference, semantic, and derived edges.
- The store is revision-aware: queries, projections, and integrity checks operate against explicit revisions rather than mutable in-place state.

## Related atoms

### Depends on

- [depends_on:: [[transaction-log]]]
- [depends_on:: [[content-addressed-store]]]
- [depends_on:: [[document-head]]]
- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[revision]]]
- [supports:: [[transaction]]]
- [supports:: [[projection]]]
- [supports:: [[query-engine]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: core
id: query-engine
title: Query engine
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-query
provenance: source docs/core/interfaces.md
---

# Query engine

## Answer

The query engine executes revision-aware retrieval over canonical graphs, histories, diffs, and derived projections without becoming the source of truth itself.

## Supporting points

- Queries must resolve against an explicit revision or document head.
- The engine should unify structural traversal, history inspection, diffing, logical facts, and semantic lookups under query plans.
- Query execution may use indexes, semantic providers, and graph materializations, but correctness remains anchored in canonical revisions.
- The engine is allowed to compose structural and semantic retrieval, but it must explain provenance for each result.

## Related atoms

### Depends on

- [depends_on:: [[graph-store]]]
- [depends_on:: [[projection-spec]]]
- [depends_on:: [[semantic-indexing]]]
- [depends_on:: [[revision]]]

### Supports

- [supports:: [[kernel-api]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]
- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

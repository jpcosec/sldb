---
layer: store
id: derived-index
title: Derived index
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-indexes
provenance: source docs/architecture/target-system-overview.md
---

# Derived index

## Answer

A derived index is any materialized query-oriented or projection-oriented index built from the canonical graph store rather than acting as source of truth.

## Supporting points

- Section, field, search, and semantic indexes are derived indexes.
- They are rebuildable from canonical state.
- They preserve the current store discipline while changing the backend.

## Related atoms

### Depends on

- [depends_on:: [[graph-store]]]

### Supports

- [supports:: [[section-index]]]
- [supports:: [[field-index]]]
- [supports:: [[search-projection]]]
- [supports:: [[semantic-indexing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

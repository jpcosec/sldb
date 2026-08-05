---
layer: core
id: cache
title: Cache
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-hashing
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Cache

## Answer

Cache stores rebuildable derived artifacts keyed from canonical structure and dependency-aware invalidation.

## Supporting points

- It should rely on canonical hashes and dependencies rather than ad hoc timestamps.
- It belongs to infrastructure, not document truth.
- It accelerates repeated projections and queries.

## Related atoms

### Depends on

- [depends_on:: [[dependency-index]]]
- [depends_on:: [[node-hash]]]

### Supports

- [supports:: [[projection]]]
- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

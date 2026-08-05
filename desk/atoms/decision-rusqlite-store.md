---
layer: store
id: decision-rusqlite-store
title: Decision store backend behind trait
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/core/libraries_core.md
---

# Decision store backend behind trait

## Answer

The kernel must own a `StorageBackend` boundary and avoid baking SQLite-specific behavior into the canonical model. `rusqlite` is no longer the governing decision.

## Supporting points

- The new architecture treats backend choice as replaceable infrastructure.
- `redb` is the default embedded direction for the controlled kernel path.
- `CozoDB` remains a valid prototyping backend when faster graph/query experimentation is worth the tradeoff.
- Transaction semantics, revisions, hashes, and capabilities must stay invariant across backend swaps.

## Related atoms

### Supports

- [supports:: [[store-infrastructure]]]
- [supports:: [[graph-store]]]
- [supports:: [[ports-and-adapters]]]

### Constrains

- [constrains:: [[transaction-log]]]
- [constrains:: [[content-addressed-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

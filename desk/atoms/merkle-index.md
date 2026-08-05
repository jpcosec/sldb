---
layer: store
id: merkle-index
title: Merkle index
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-hashing
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Merkle index

## Answer

The Merkle index organizes node and subtree hashes into a structural integrity and incremental recomputation layer over canonical content.

## Supporting points

- It makes structural hashing operational.
- It enables subtree integrity and dependency-aware rebuilds.
- It should derive from canonical structure rather than file timestamps.

## Related atoms

### Depends on

- [depends_on:: [[node-hash]]]
- [depends_on:: [[dependency-index]]]

### Supports

- [supports:: [[cache]]]
- [supports:: [[store-integrity-checks]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Depends on
- [depends_on:: [[rust-core]]]

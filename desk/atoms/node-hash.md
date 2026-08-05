---
layer: core
id: node-hash
title: Node hash
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-hashing
provenance: source docs/core/diagramas_core.md
---

# Node hash

## Answer

A node hash is the deterministic Merkle fingerprint computed from canonical node data plus the hashes of structurally owned children.

## Supporting points

- Structural hashing is lazy: dirty branches are invalidated on change and recomputed only when queried, committed, exported, or verified.
- Only ownership edges participate recursively in the structural Merkle so references and semantic cycles cannot break hashing.
- The same canonical content must always produce the same hash.
- Hash caches are rebuildable accelerators, not sources of truth.

## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[content-addressed-store]]]
- [depends_on:: [[source-document-hash]]]

### Supports

- [supports:: [[store-integrity-checks]]]
- [supports:: [[projection]]]
- [supports:: [[revision]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

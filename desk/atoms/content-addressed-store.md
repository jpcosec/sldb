---
layer: store
id: content-addressed-store
title: Content-addressed store
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-persistence
- domain:store-hashing
provenance: source docs/core/diagramas_core.md
---

# Content-addressed store

## Answer

The content-addressed store persists payloads and derived artifacts under deterministic hashes so content identity stays decoupled from mutable locations.

## Supporting points

- The same canonical bytes should map to the same stored hash key.
- Payload storage supports deduplication, integrity verification, and lazy retrieval.
- Canonical node hashes and revision hashes may reference content-addressed payloads without duplicating them inline.

## Related atoms

### Depends on

- [depends_on:: [[node-hash]]]
- [depends_on:: [[provenance-record]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[projection]]]
- [supports:: [[document-materializer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

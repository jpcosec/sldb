---
layer: store
id: storage-backend
title: Storage backend
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-persistence
- domain:architecture-integration
provenance: source docs/core/interfaces.md
---

# Storage backend

## Answer

A storage backend is the replaceable persistence adapter that implements the kernel repository contracts for logs, revisions, heads, and content-addressed payloads.

## Supporting points

- redb, Cozo, and in-memory stores are backend strategies, not kernel identity.
- Storage contracts must preserve atomic commit, replayability, and revision integrity.
- Backend swaps must not change canonical hashing or transaction semantics.

## Related atoms

### Depends on

- [depends_on:: [[ports-and-adapters]]]
- [depends_on:: [[transaction-log]]]
- [depends_on:: [[content-addressed-store]]]
- [depends_on:: [[document-head]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[store-infrastructure]]]
- [supports:: [[decision-rusqlite-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

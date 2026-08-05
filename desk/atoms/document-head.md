---
layer: store
id: document-head
title: Document head
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-graph
- domain:runtime-revisions
provenance: source docs/core/diagramas_core.md
---

# Document head

## Answer

A document head is the mutable pointer from a document identity to its current revision, updated by compare-and-swap during commit.

## Supporting points

- Heads are the narrow mutable coordination point in an otherwise immutable revision model.
- Optimistic concurrency and conflict detection depend on compare-and-swap semantics over heads.
- A head is not the source of truth by itself; it points into immutable revision and transaction history.

## Related atoms

### Depends on

- [depends_on:: [[document]]]
- [depends_on:: [[revision]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[transaction]]]
- [supports:: [[query-engine]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

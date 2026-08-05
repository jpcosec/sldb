---
layer: core
id: ast-persistence
title: AST persistence
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-graph
provenance: source docs/architecture/target-system-overview.md
---

# AST persistence

## Answer

AST persistence is the durable storage of canonical AST nodes and their core data in the local graph store.

## Supporting points

- It ensures canonical state survives on disk.
- It must use existing libraries rather than ad hoc invention.
- It is part of the graph-store design.

## Related atoms

### Depends on

- [depends_on:: [[graph-store]]]

### Supports

- [supports:: [[canonical-existence]]]
- [supports:: [[document-tracker]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

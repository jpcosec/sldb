---
layer: store
id: dependency-index
title: Dependency index
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-indexes
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Dependency index

## Answer

A dependency index records structural and derived dependencies so recomputation, validation, and projection updates can happen incrementally.

## Supporting points

- It supports precise invalidation and rebuild behavior.
- It belongs beside the AST as infrastructure.
- It is essential for scalable projection and cache logic.

## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[node-hash]]]

### Supports

- [supports:: [[cache]]]
- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

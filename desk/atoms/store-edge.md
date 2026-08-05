---
layer: store
id: store-edge
title: Store edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Store edge

## Answer

A store edge is the canonical edge type that records store-level relationships between ASTs in the graph store.

## Supporting points

- It is part of how the store connects canonical units.
- It belongs to the graph store rather than the rendered document surface.
- It helps express graph-native store semantics.

## Related atoms

### Depends on

- [depends_on:: [[store-infrastructure]]]
- [depends_on:: [[relation-ast]]]

### Supports

- [supports:: [[graph-store]]]
- [supports:: [[document-tracker]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

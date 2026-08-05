---
layer: core
id: dependency-edge
title: Dependency edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Dependency edge

## Answer

A dependency edge is the canonical edge type that expresses structural, projection, or recomputation dependency between canonical units.

## Supporting points

- It supports incremental rebuild and invalidation.
- It is part of the graph-native runtime model.
- It helps connect canonical structure to derived infrastructure.

## Related atoms

### Depends on

- [depends_on:: [[relation-ast]]]

### Supports

- [supports:: [[dependency-index]]]
- [supports:: [[cache]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

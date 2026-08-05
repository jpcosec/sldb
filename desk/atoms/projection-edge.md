---
layer: core
id: projection-edge
title: Projection edge
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Projection edge

## Answer

A projection edge is the canonical edge type that connects a canonical unit to one of its derived outputs, materializations, or projection artifacts.

## Supporting points

- It helps track which derived views come from which canonical source.
- It belongs to the graph-native runtime model.
- It supports explainable projection lineage.

## Related atoms

### Depends on

- [depends_on:: [[relation-ast]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[document-materializer]]]
- [supports:: [[graph-projection]]]
- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

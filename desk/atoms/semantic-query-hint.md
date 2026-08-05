---
layer: shared
id: semantic-query-hint
title: Semantic query hint
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Semantic query hint

## Answer

A semantic query hint is a semantic-layer aid that helps retrieval or projection systems interpret likely conceptual matches or neighborhoods.

## Supporting points

- It is an aid to semantic retrieval, not canonical truth.
- It can remain lightweight in the initial system.
- It supports richer semantic search later.

## Related atoms

### Depends on

- [depends_on:: [[concept-binding]]]

### Supports

- [supports:: [[query-engine]]]
- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

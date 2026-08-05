---
layer: shared
id: semantic-reference
title: Semantic reference
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-semantic
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Semantic reference

## Answer

A semantic reference is a semantic-layer link from one canonical unit or concept-bearing unit to another.

## Supporting points

- It is not the same as an ordinary document link.
- It belongs to the semantic relation layer.
- It is useful for richer future navigation and export.

## Related atoms

### Depends on

- [depends_on:: [[concept-binding]]]

### Supports

- [supports:: [[semantic-exporter]]]
- [supports:: [[search-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

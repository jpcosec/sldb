---
layer: core
id: source-locator
title: Source locator
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Source locator

## Answer

A source locator is the pointer mechanism used to identify where an anchor targets content in a source document or artifact.

## Supporting points

- Its concrete form depends on document family.
- It may point by text span, AST path, page, DOM location, syntax node, or similar.
- It is a core part of anchoring behavior.

## Related atoms

### Depends on

- [depends_on:: [[external-anchor]]]

### Supports

- [supports:: [[text-locator]]]
- [supports:: [[ast-locator]]]
- [supports:: [[page-locator]]]
- [supports:: [[dom-locator]]]
- [supports:: [[syntax-locator]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: shared
id: document-path
title: Document path
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Document path

## Answer

A document path is the source-path field carried by an anchor so the system knows which external document or file the anchor refers to.

## Supporting points

- It is mandatory for external anchoring.
- It complements locators and hashes.
- It is not sufficient by itself to guarantee attachment stability.

## Related atoms

### Depends on

- [depends_on:: [[external-anchor]]]

### Supports

- [supports:: [[text-anchor]]]
- [supports:: [[ast-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

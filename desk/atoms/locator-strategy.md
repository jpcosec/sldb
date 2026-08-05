---
layer: shared
id: locator-strategy
title: Locator strategy
five_wh_one_plus: how
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Locator strategy

## Answer

A locator strategy is the document-family-specific method used to point to source content for anchoring or recovery.

## Supporting points

- Different families need different locator forms.
- It is a core part of anchoring design.
- It separates generic anchoring from family-specific implementation.

## Related atoms

### Depends on

- [depends_on:: [[source-locator]]]

### Supports

- [supports:: [[text-locator]]]
- [supports:: [[ast-locator]]]
- [supports:: [[page-locator]]]
- [supports:: [[dom-locator]]]
- [supports:: [[syntax-locator]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

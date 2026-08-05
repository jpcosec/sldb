---
layer: shared
id: source-document-hash
title: Source document hash
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Source document hash

## Answer

A source document hash is the source-file hash stored with an anchor so the system can detect changes in the anchored external document.

## Supporting points

- It supports change detection across external files.
- It is one of the mandatory evidentiary anchor fields.
- It complements sample text and locators.

## Related atoms

### Depends on

- [depends_on:: [[text-anchor]]]

### Supports

- [supports:: [[external-anchor-resolver]]]
- [supports:: [[hash-field]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

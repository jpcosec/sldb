---
layer: shell
id: link-editor
title: Link editor
five_wh_one_plus: what
tags:
- system:sldb
- domain:surfaces-visual-inspectors
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Link editor

## Answer

The link editor is the UX component that supports creating, inspecting, and modifying links and transclusions against canonical targets.

## Supporting points

- It is a visual editing companion to canonical link semantics.
- It depends on stable targeting and link relations.
- It should expose links as first-class structured operations.

## Related atoms

### Depends on

- [depends_on:: [[visual-ux-surface]]]
- [depends_on:: [[link-reference]]]
- [depends_on:: [[transclusion-reference]]]

### Supports

- [supports:: [[local-anchor-resolver]]]
- [supports:: [[external-anchor-resolver]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

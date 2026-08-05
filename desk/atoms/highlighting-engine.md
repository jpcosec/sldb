---
layer: shell
id: highlighting-engine
title: Highlighting engine
five_wh_one_plus: what
tags:
- system:sldb
- domain:surfaces-visual-inspectors
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Highlighting engine

## Answer

The highlighting engine is the UX component that renders structural, semantic, and model-aware emphasis over canonical or projected content.

## Supporting points

- It should support syntax, semantics, fields, links, and anchors.
- It is a UX projection layer rather than a canonical data layer.
- It helps users inspect the model in context.

## Related atoms

### Depends on

- [depends_on:: [[visual-ux-surface]]]
- [depends_on:: [[prosemirror-adapter]]]

### Supports

- [supports:: [[link-editor]]]
- [supports:: [[model-browser]]]
- [supports:: [[template-browser]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

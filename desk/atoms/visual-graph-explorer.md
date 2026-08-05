---
layer: shell
id: visual-graph-explorer
title: Visual graph explorer
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-visual-inspectors
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Visual graph explorer

## Answer

The visual graph explorer is the UX component that lets users inspect graph-derived relations between documents, nodes, fields, anchors, and semantic structures.

## Supporting points

- It is one of the major future UX surfaces.
- It depends on graph projections rather than raw text parsing.
- It should share canonical identity with CLI and editor views.

## Related atoms

### Depends on

- [depends_on:: [[visual-ux-surface]]]
- [depends_on:: [[graph-projection]]]

### Supports

- [supports:: [[model-browser]]]
- [supports:: [[template-browser]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

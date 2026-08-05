---
layer: shell
id: local-anchor-resolver
title: Local anchor resolver
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-resolvers
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Local anchor resolver

## Answer

The local anchor resolver maps local selectors, fragments, and anchors to canonical nodes inside the current document space.

## Supporting points

- It resolves intra-document targeting.
- It supports links, navigation, and editor inspection.
- It should rely on canonical selectors rather than raw text positions alone.

## Related atoms

### Depends on

- [depends_on:: [[addressability-layer]]]
- [depends_on:: [[stable-selector]]]

### Supports

- [supports:: [[link-reference]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

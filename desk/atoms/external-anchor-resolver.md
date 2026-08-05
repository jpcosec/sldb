---
layer: shell
id: external-anchor-resolver
title: External anchor resolver
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-resolvers
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# External anchor resolver

## Answer

The external anchor resolver uses evidence, locators, text samples, and fingerprints to reattach references to content outside the local canonical document.

## Supporting points

- It handles drift-prone external targets.
- It should combine selector logic with anchoring evidence.
- It is distinct from local address resolution.

## Related atoms

### Depends on

- [depends_on:: [[addressability-layer]]]
- [depends_on:: [[external-anchor]]]

### Supports

- [supports:: [[text-as-graph]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

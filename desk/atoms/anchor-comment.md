---
layer: shell
id: anchor-comment
title: Anchor comment
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Anchor comment

## Answer

An anchor comment is optional commentary attached to an anchor to explain its intent, ambiguity, or usage context.

## Supporting points

- Comments enrich anchor interpretation without changing target identity.
- They are useful for human-facing inspection and UX.
- They belong to anchor payload structure.

## Related atoms

### Depends on

- [depends_on:: [[external-anchor]]]

### Supports

- [supports:: [[text-anchor]]]
- [supports:: [[ast-anchor]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

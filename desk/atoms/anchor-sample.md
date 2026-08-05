---
layer: core
id: anchor-sample
title: Anchor sample
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Anchor sample

## Answer

An anchor sample is the quoted text evidence carried by a text-oriented anchor to support reattachment and drift detection.

## Supporting points

- It is one of the key evidence fields of a text anchor.
- It helps the system detect whether the cited source changed.
- It is not the only anchor field; it works with path, hash, and locator.

## Related atoms

### Depends on

- [depends_on:: [[text-anchor]]]

### Supports

- [supports:: [[external-anchor-resolver]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

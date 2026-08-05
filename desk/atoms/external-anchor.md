---
layer: shell
id: external-anchor
title: External Anchor
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# External Anchor

## Answer

An external anchor is an evidence-backed canonical attachment to content outside the local document.

## Supporting points

- External anchoring is separate from local tree structure and must be modeled explicitly.
- Durable external anchors require locator data, sampled text or context, and content fingerprint evidence.
- Reattachment policy and confidence belong to the anchoring concept because external targets can drift.
## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[canonical-identity]]]

### Supports

- [supports:: [[stable-selector]]]
- [supports:: [[visual-ux-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

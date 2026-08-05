---
layer: core
id: local-anchor
title: Local anchor
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Local anchor

## Answer

A local anchor is a document-internal targeting unit used to address canonical content within the local AST space.

## Supporting points

- It is distinct from external anchoring.
- It supports intra-document links, navigation, and inspection.
- It belongs to the canonical addressability model.

## Related atoms

### Depends on

- [depends_on:: [[addressability-layer]]]
- [depends_on:: [[stable-selector]]]

### Supports

- [supports:: [[local-anchor-resolver]]]
- [supports:: [[link-reference]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

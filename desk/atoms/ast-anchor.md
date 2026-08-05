---
layer: core
id: ast-anchor
title: AST anchor
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# AST anchor

## Answer

An AST anchor is an anchor node that targets source content through structural or AST-aware addressing rather than plain text alone.

## Supporting points

- It is used for structured families with stable structural identity.
- It is one canonical anchor kind.
- It supports structure-aware tracking across changes.

## Related atoms

### Depends on

- [depends_on:: [[external-anchor]]]
- [depends_on:: [[source-locator]]]

### Supports

- [supports:: [[canonical-address]]]
- [supports:: [[document-path]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

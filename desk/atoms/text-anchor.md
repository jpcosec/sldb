---
layer: shell
id: text-anchor
title: Text anchor
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Text anchor

## Answer

A text anchor is an anchor node that targets source content through text-oriented evidence such as quoted sample, hash, and locator.

## Supporting points

- It is used when text is the relevant anchoring surface.
- It supports drift detection through evidence-bearing attachment.
- It is one canonical anchor kind.

## Related atoms

### Depends on

- [depends_on:: [[external-anchor]]]
- [depends_on:: [[source-locator]]]

### Supports

- [supports:: [[anchor-sample]]]
- [supports:: [[source-document-hash]]]
- [supports:: [[document-path]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

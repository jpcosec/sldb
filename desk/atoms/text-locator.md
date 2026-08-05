---
layer: core
id: text-locator
title: Text locator
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Text locator

## Answer

A text locator is a locator strategy based on textual positions or spans such as character, paragraph, or nearby context.

## Supporting points

- It is suitable for plain text-like families.
- It supports text anchors.
- It is one locator specialization.

## Related atoms

### Depends on

- [depends_on:: [[locator-strategy]]]

### Supports

- [supports:: [[text-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

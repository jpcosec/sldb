---
layer: core
id: page-locator
title: Page locator
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Page locator

## Answer

A page locator is a locator strategy based on page-oriented source addressing.

## Supporting points

- It is useful for PDFs and similar formats.
- It is one locator specialization.
- It supports non-reversible families.

## Related atoms

### Depends on

- [depends_on:: [[locator-strategy]]]

### Supports

- [supports:: [[non-reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

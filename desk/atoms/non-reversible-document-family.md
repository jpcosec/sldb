---
layer: core
id: non-reversible-document-family
title: Non-reversible document family
five_wh_one_plus: when
tags:
- system:sldb
- domain:model-documents
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Non-reversible document family

## Answer

A non-reversible document family is a family of documents for which SLDB may only support partial structure or family-specific anchoring rather than a fully reversible render cycle.

## Supporting points

- These families can still participate in anchoring and indexing.
- They use family-specific structure or locators where available.
- They are not the primary baseline for exact round-trip recreation.

## Related atoms

### Depends on

- [depends_on:: [[source-locator]]]

### Supports

- [supports:: [[locator-strategy]]]
- [supports:: [[text-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

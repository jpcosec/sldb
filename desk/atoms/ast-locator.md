---
layer: core
id: ast-locator
title: AST locator
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# AST locator

## Answer

An AST locator is a locator strategy based on structural or AST-aware addressing inside a structured source family.

## Supporting points

- It is suitable for reversible or structure-rich families.
- It supports AST anchors.
- It is one locator specialization.

## Related atoms

### Depends on

- [depends_on:: [[locator-strategy]]]

### Supports

- [supports:: [[ast-anchor]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

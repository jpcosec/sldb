---
layer: core
id: syntax-locator
title: Syntax locator
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-anchors
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Syntax locator

## Answer

A syntax locator is a locator strategy based on syntax-aware structures such as tree-sitter nodes in code-like sources.

## Supporting points

- It is suitable for code families.
- It is one locator specialization.
- It supports structure-aware external anchoring for code.

## Related atoms

### Depends on

- [depends_on:: [[locator-strategy]]]

### Supports

- [supports:: [[tree-sitter-adapter]]]
- [supports:: [[non-reversible-document-family]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

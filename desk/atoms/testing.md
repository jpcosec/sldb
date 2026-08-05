---
layer: shell
id: testing
title: Testing
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-testing-generic
provenance: source docs/architecture/ritual-testing.md
---

# Testing

## Answer

Testing is the validation dimension that must cover both unit-level correctness and UX-level behavior for the refactored SLDB system.

## Supporting points

- Unit testing proves the contracts of AST structure, field binding, links, projections, and store-facing behavior.
- UX testing proves the recognizable behavior of CLI workflows and future visual interactions.
- This dimension lets the knowledge base connect implementation structure with observable product validation.

## Related atoms

### Supports

- [supports:: [[rust-testing]]]
- [supports:: [[python-testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

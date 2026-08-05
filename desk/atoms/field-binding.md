---
layer: shared
id: field-binding
title: Field Binding
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-fields-schemas
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Field Binding

## Answer

Field binding connects canonical structure to typed document-model semantics.

## Supporting points

- The refactor preserves the original SLDB promise around typed models rather than abandoning it.
- One or more AST nodes may bind to typed fields without making field contracts the only structure.
- Extraction, rendering, validation, reversibility, and composition depend on explicit field binding.
## Related atoms

### Depends on

- [depends_on:: [[canonical-ast]]]
- [depends_on:: [[node]]]

### Supports

- [supports:: [[field-path]]]
- [supports:: [[schema-binding]]]
- [supports:: [[type-contract]]]
- [supports:: [[structurednldoc-contract]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

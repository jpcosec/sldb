---
layer: shared
id: type-contract
title: Type Contract
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-fields-schemas
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Type Contract

## Answer

Type contract records the expected type and validation semantics for bound canonical content.

## Supporting points

- The AST preserves expected type information rather than treating content as opaque text.
- Validation and rendering continuity depend on explicit type-aware contracts.
- Requiredness, defaults, cardinality, and other typed constraints are downstream of this contract layer.
## Related atoms

### Depends on

- [depends_on:: [[schema-binding]]]
- [depends_on:: [[field-binding]]]

### Supports

- [supports:: [[structurednldoc-contract]]]
- [supports:: [[payload-input-forms]]]
- [supports:: [[field-descriptions-are-required-contract]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

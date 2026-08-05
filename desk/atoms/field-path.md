---
layer: shared
id: field-path
title: Field Path
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-fields-schemas
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Field Path

## Answer

Field path gives a durable way to locate a field within nested model composition.

## Supporting points

- The canonical model requires field-path awareness.
- Nested composition and multi-level typed structures depend on stable field paths.
- Precise provenance, validation, and visual inspection need field-level addressability.
## Related atoms

### Depends on

- [depends_on:: [[field-binding]]]
- [depends_on:: [[schema-binding]]]

### Supports

- [supports:: [[field-and-section-navigation]]]
- [supports:: [[tracked-document-identity]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

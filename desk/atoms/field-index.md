---
layer: store
id: field-index
title: Field index
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-indexes
provenance: source docs/sldb-v1/faq.md
---

# Field index

## Answer

The field index organizes field-level bindings and values for targeted lookup, navigation, and update flows.

## Supporting points

- It is the retrieval surface for field-aware workflows.
- It depends on explicit field binding.
- It should stay derived from canonical structure and schema semantics.

## Related atoms

### Depends on

- [depends_on:: [[field-binding]]]
- [depends_on:: [[search-projection]]]

### Supports

- [supports:: [[field-and-section-navigation]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

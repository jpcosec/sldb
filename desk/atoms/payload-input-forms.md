---
layer: shell
id: payload-input-forms
title: Payload input forms
five_wh_one_plus: how
tags:
- system:sldb
- domain:surfaces-cli-inputs-outputs
provenance: source docs/sldb-v1/faq.md
---

# Payload input forms

## Answer

Create, update, and render workflows accept payload data either inline or from a JSON or YAML file path, and the payload must conform to the target model schema.

## Supporting points

- The CLI accepts both inline and file-based payload entry.
- This is part of the ergonomic contract of the product.
- Schema conformance remains part of the observable behavior.
## Related atoms

### Depends on

- [depends_on:: [[structurednldoc-contract]]]
- [depends_on:: [[type-contract]]]

### Supports

- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: shared
id: shallow-title-plus-body-default
title: Shallow `title + body` default
five_wh_one_plus: when
tags:
- system:sldb
- domain:model-text-structure
provenance: source docs/sldb-v1/faq.md
---

# Shallow `title + body` default

## Answer

For heterogeneous narrative documents, the recommended default is a shallow `title + body` model unless richer typed structure is truly needed.

## Supporting points

- This is the documented authoring default for many real-world docs.
- It keeps modeling lightweight where deep structure is unnecessary.
- The refactor should preserve this practical modeling guidance.
## Related atoms

### Depends on

- [depends_on:: [[structurednldoc-contract]]]

### Supports

- [supports:: [[lead-paragraph-anchor-rule]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

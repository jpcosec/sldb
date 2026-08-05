---
layer: store
id: section-index
title: Section index
five_wh_one_plus: what
tags:
- system:sldb
- domain:store-indexes
provenance: source docs/sldb-v1/faq.md
---

# Section index

## Answer

The section index is the retrieval component that organizes section-level canonical structure for navigation, querying, and inspection.

## Supporting points

- It supports deeper navigation than whole-document access.
- It should be derived from canonical structure.
- It belongs to retrieval infrastructure rather than document truth.

## Related atoms

### Depends on

- [depends_on:: [[tree-spine]]]
- [depends_on:: [[search-projection]]]

### Supports

- [supports:: [[field-and-section-navigation]]]
- [supports:: [[semantic-vs-physical-search]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

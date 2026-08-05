---
layer: shell
id: physical-search
title: Physical search
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Physical search

## Answer

Use physical search when the query is path-like, name-like, or structure-like and should match concrete tracked artifacts rather than semantic tags.

## Supporting points

- It is suited to known paths, names, and structural tokens.
- It complements semantic retrieval instead of replacing it.
- It should remain distinct from semantic lookup in the refactor.

## Related atoms

### Supports

- [supports:: [[tracked-document-identity]]]

### Contrasts with

- [contrasts_with:: [[semantic-search]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

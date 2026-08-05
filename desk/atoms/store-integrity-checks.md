---
layer: store
id: store-integrity-checks
title: Store integrity checks
five_wh_one_plus: how
tags:
- system:sldb
- domain:store-integrity
provenance: source docs/sldb-v1/faq.md
---

# Store integrity checks

## Answer

`stores check` reports drift or breakage in tracked state without modifying content, and `stores update` rebuilds indexes after bulk changes.

## Supporting points

- The external promise is diagnostic and maintenance behavior.
- Users rely on check for integrity and update for rebuilds.
- The atom should preserve purpose rather than freeze internal hash layout.

## Related atoms

### Implements with

- [implements_with:: [[node-hash]]]
- [implements_with:: [[provenance-record]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

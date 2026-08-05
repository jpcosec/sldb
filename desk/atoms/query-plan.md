---
layer: shared
id: query-plan
title: Query plan
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/core/core_README.md
---

# Query plan

## Answer

A query plan is the explicit intermediate representation of retrieval intent before the kernel executes structural, historical, logical, or semantic lookup.

## Supporting points

- Query plans keep host syntax separate from kernel evaluation semantics.
- They should bind revision context, filters, traversal shape, and output expectations.
- Query planning prevents one client DSL from becoming hidden query authority.

## Related atoms

### Depends on

- [depends_on:: [[query-engine]]]

### Supports

- [supports:: [[lisp-metalanguage]]]
- [supports:: [[kernel-api]]]
- [supports:: [[observability-surface]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

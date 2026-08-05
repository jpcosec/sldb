---
layer: shared
id: projection-plan
title: Projection plan
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/core/core_README.md
---

# Projection plan

## Answer

A projection plan is the explicit request for building a derived view from canonical revision state under a declared specification and engine version.

## Supporting points

- Projection plans cover rendered documents, structural views, semantic views, and other derived outputs.
- They keep projection inputs, revision scope, and output intent visible.
- Derived projections remain rebuildable and non-sovereign even when heavily cached.

## Related atoms

### Depends on

- [depends_on:: [[projection]]]
- [depends_on:: [[projection-spec]]]

### Supports

- [supports:: [[lisp-metalanguage]]]
- [supports:: [[projection-engine]]]
- [supports:: [[renderer]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

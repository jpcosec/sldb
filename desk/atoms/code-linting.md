---
layer: shell
id: code-linting
title: Code linting
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-clean-code-generic
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Code linting

## Answer

Code linting is the clean-code dimension that keeps the refactor readable, constrained, low-clutter, and structurally aligned with the intended architecture.

## Supporting points

- This dimension is about architectural cleanliness, naming, duplication control, and surface clarity, not only formatter output.
- It should prevent accidental complexity from reappearing between the AST core, projections, store infrastructure, and CLI surfaces.
- It gives the knowledge base a way to connect product cleanliness expectations with implementation review criteria.

## Related atoms

### Supports

- [supports:: [[rust-code-linting]]]
- [supports:: [[python-code-linting]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

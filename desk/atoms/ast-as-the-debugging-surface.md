---
layer: shell
id: ast-as-the-debugging-surface
title: AST as the debugging surface
five_wh_one_plus: where
tags:
- system:sldb
- domain:runtime-query
provenance: source docs/sldb-v1/faq.md
---

# AST as the debugging surface

## Answer

`ast show` is the primary user-facing debugging surface when query, section, or ownership results do not match expectations.

## Supporting points

- The AST view is the main normalization and inspection surface for debugging.
- This is a durable usage pattern in the docs.
- The exact schema may evolve, but the debugging role should survive.

## Related atoms

### Supports

- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

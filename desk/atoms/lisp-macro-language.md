---
layer: shared
id: lisp-macro-language
title: Lisp macro language
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/core/core_README.md
---

# Lisp macro language

## Answer

The Lisp macro language is an authored input surface used to express reusable functional behavior that lowers into kernel-validated plans rather than mutating canonical state directly.

## Supporting points

- Macros are for functionality, composition, and reuse.
- Macro expansion does not bypass Rust-owned validation, typing, capability checks, or transaction rules.
- Authored macro forms are inputs; any later emitted Lisp representation from canonical state is a materialization.
- Macro forms should be translatable or hostable by other surfaces without changing kernel authority.

## Related atoms

### Depends on

- [depends_on:: [[rust-core]]]
- [depends_on:: [[lisp-metalanguage]]]
- [depends_on:: [[transaction-plan]]]
- [depends_on:: [[effect-plan]]]

### Supports

- [supports:: [[query-plan]]]
- [supports:: [[projection-plan]]]
- [supports:: [[hook-runtime]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

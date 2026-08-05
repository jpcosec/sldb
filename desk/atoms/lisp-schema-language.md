---
layer: shared
id: lisp-schema-language
title: Lisp schema language
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-fields-schemas
provenance: source docs/core/core_README.md
---

# Lisp schema language

## Answer

The Lisp schema language is an authored input surface used to define inspectable schema and model contracts that the Rust kernel validates and interprets.

## Supporting points

- Lisp schema forms describe structure and constraints without becoming canonical persistence by themselves.
- Schema meaning is owned by the Rust kernel, not by a standalone Lisp runtime.
- Authored schema forms are inputs; any exported Lisp form later emitted from canonical state is a materialization.
- Schema forms should remain translatable to other surfaces without changing kernel truth.

## Related atoms

### Depends on

- [depends_on:: [[rust-core]]]
- [depends_on:: [[schema-binding]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[lisp-metalanguage]]]
- [supports:: [[type-contract]]]
- [supports:: [[structurednldoc-contract]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

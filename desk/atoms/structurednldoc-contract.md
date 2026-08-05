---
layer: shared
id: structurednldoc-contract
title: StructuredNLDoc contract
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-documents
provenance: source docs/sldb-v1/faq.md
---

# StructuredNLDoc contract

## Answer

A `StructuredNLDoc` defines the structured text template, typed Lisp schema fields, field descriptions, and optional semantics that make text-to-payload-to-text workflows possible.

## Supporting points

- This is the central user-facing document-model contract in v1.
- Typed fields and template structure are both part of the public behavior.
- The refactor generalizes this contract rather than discarding it.

## Related atoms

### Supports

- [supports:: [[python-patterns]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

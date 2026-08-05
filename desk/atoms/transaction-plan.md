---
layer: shared
id: transaction-plan
title: Transaction plan
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-boundaries
provenance: source docs/core/core_README.md
---

# Transaction plan

## Answer

A transaction plan is the validated intermediate representation of intended mutation before it becomes a committed transaction.

## Supporting points

- Lisp, CLI, UI, or agents may propose transaction plans, but the kernel alone validates and commits them.
- A transaction plan should name base revision, operations, actor context, and required capabilities.
- Plans preserve explicit intent without granting direct write authority to clients.

## Related atoms

### Depends on

- [depends_on:: [[transaction]]]
- [depends_on:: [[capability-model]]]

### Supports

- [supports:: [[lisp-metalanguage]]]
- [supports:: [[kernel-api]]]
- [supports:: [[primitive-operation]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: core
id: transaction
title: Transaction
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-transactions
provenance: source docs/core/reasoning.md
---

# Transaction

## Answer

A transaction is the only authorized unit of mutation: a validated, ordered set of primitive operations applied against a base revision to produce a new revision.

## Supporting points

- Transactions carry actor identity, base revision, required capabilities, and the operations to stage.
- Validation must happen before commit, including type checks, invariants, and conflict checks.
- A transaction appends to the log, writes revision state, updates document head, and emits events atomically.
- External effects are never executed inside the transaction itself.

## Related atoms

### Depends on

- [depends_on:: [[primitive-operation]]]
- [depends_on:: [[revision]]]
- [depends_on:: [[capability-model]]]

### Supports

- [supports:: [[rust-core]]]
- [supports:: [[transaction-log]]]
- [supports:: [[event-bus]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

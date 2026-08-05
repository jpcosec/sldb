---
layer: shared
id: failure-model
title: Failure model
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-reliability
provenance: source docs/core/also_core.md
---

# Failure model

## Answer

The failure model classifies kernel and adapter failures into stable categories so recovery, retries, user reporting, and corruption handling follow explicit rules.

## Supporting points

- At minimum it distinguishes recoverable error, permanent error, conflict, degraded mode, and corruption.
- Failure handling must cover parser, transaction, persistence, renderer, hook, agent, Git, and process-crash paths.
- Failure categories are part of the product contract, not just logging detail.

## Related atoms

### Supports

- [supports:: [[degraded-mode]]]
- [supports:: [[corruption-state]]]
- [supports:: [[store-recovery]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

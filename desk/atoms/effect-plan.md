---
layer: shared
id: effect-plan
title: Effect plan
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-boundaries
- domain:runtime-hooks
provenance: source docs/core/core_README.md
---

# Effect plan

## Answer

An effect plan is the explicit request for an external action that must pass capability checks and execute outside canonical transactions.

## Supporting points

- Effect plans describe intended side effects without letting them mutate canonical state inline.
- They should capture requested action, capabilities, provenance, and expected result shape.
- Executed effect results re-enter the kernel only through later transactions or status records.

## Related atoms

### Depends on

- [depends_on:: [[capability-model]]]
- [depends_on:: [[effect-outbox]]]

### Supports

- [supports:: [[lisp-metalanguage]]]
- [supports:: [[hook-runtime]]]
- [supports:: [[agent-provider]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

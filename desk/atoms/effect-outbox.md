---
layer: shell
id: effect-outbox
title: Effect outbox
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-hooks
- domain:runtime-effects
provenance: source docs/core/diagramas_core.md
---

# Effect outbox

## Answer

The effect outbox is the persistent queue of approved external actions that must run after commit and report their results back through later transactions.

## Supporting points

- Outboxed effects isolate the kernel from partial writes caused by Git, filesystem, process, network, or agent failures.
- An effect entry should include the requested action plan, capabilities, provenance, and execution status.
- External side effects and their results become auditable kernel history rather than invisible runtime behavior.

## Related atoms

### Depends on

- [depends_on:: [[capability-model]]]
- [depends_on:: [[transaction-log]]]

### Supports

- [supports:: [[hook-runtime]]]
- [supports:: [[provenance-record]]]
- [supports:: [[append-only-event-log]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

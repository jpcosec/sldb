---
layer: shell
id: event-bus
title: Event bus
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-hooks
- domain:runtime-effects
provenance: source docs/core/diagramas_core.md
---

# Event bus

## Answer

The event bus publishes committed kernel events to hooks, projections, and automation surfaces without turning them into hidden mutation paths.

## Supporting points

- Events are emitted after successful transaction commit.
- Subsystems may subscribe to transaction, revision, projection, and integrity events.
- Event delivery is part of runtime orchestration, but authoritative state changes still re-enter through transactions.

## Related atoms

### Depends on

- [depends_on:: [[transaction]]]
- [depends_on:: [[append-only-event-log]]]

### Supports

- [supports:: [[hook-runtime]]]
- [supports:: [[effect-outbox]]]
- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

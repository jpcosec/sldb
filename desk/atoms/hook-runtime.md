---
layer: shell
id: hook-runtime
title: Hook runtime
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-hooks
provenance: source docs/core/reasoning.md
---

# Hook runtime

## Answer

The hook runtime interprets hook bindings over committed kernel events and turns approved actions into outboxed effects rather than mutating the graph inline.

## Supporting points

- Hooks run after transactions, not inside them.
- A hook may produce an `ActionPlan`, but execution of filesystem, Git, network, tool, or agent actions must happen through an effect outbox.
- Effect results re-enter the kernel as later transactions so failure cannot leave the canonical graph half-written.
- Capability checks belong to the hook/effect path before any external action is executed.

## Related atoms

### Depends on

- [depends_on:: [[hook-binding]]]
- [depends_on:: [[event-bus]]]
- [depends_on:: [[effect-outbox]]]
- [depends_on:: [[capability-model]]]

### Supports

- [supports:: [[kernel-api]]]
- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

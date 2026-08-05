---
layer: shell
id: agent-provider
title: Agent provider
five_wh_one_plus: how
tags:
- system:sldb
- domain:architecture-integration
- domain:runtime-effects
provenance: source docs/core/interfaces.md
---

# Agent provider

## Answer

An agent provider is the replaceable adapter through which the kernel invokes local or remote agents as capability-checked external effects.

## Supporting points

- Agent invocation is not a hidden mutation path; it produces effect requests and later effect results.
- Local subagents and MCP-style remote agents fit the same adapter role.
- Agent outputs must re-enter canonical state through transactions.

## Related atoms

### Depends on

- [depends_on:: [[effect-outbox]]]
- [depends_on:: [[capability-model]]]
- [depends_on:: [[ports-and-adapters]]]

### Supports

- [supports:: [[hook-runtime]]]
- [supports:: [[event-bus]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

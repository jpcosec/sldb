---
layer: shared
id: capability-model
title: Capability model
five_wh_one_plus: how
tags:
- system:sldb
- domain:architecture-boundaries
- domain:security-capabilities
provenance: source docs/core/core_README.md
---

# Capability model

## Answer

The capability model is the explicit permission system that governs external effects, adapters, macros, hooks, agents, and other non-trivial kernel actions.

## Supporting points

- Filesystem, Git, network, process, and agent invocation must be declared and validated explicitly.
- Capabilities belong to plans and effects, not to implicit trust in one client implementation.
- Capability checks are part of the kernel contract for safe automation.

## Related atoms

### Depends on

- [depends_on:: [[kernel-api]]]
- [depends_on:: [[effect-outbox]]]

### Supports

- [supports:: [[transaction]]]
- [supports:: [[hook-runtime]]]
- [supports:: [[effect-plan]]]
- [supports:: [[threat-model]]]
- [supports:: [[lisp-metalanguage]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

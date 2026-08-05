---
layer: shell
id: python-cli-orchestration-layer
title: Python CLI orchestration layer
five_wh_one_plus: how
tags:
- system:sldb
- domain:implementation-python-cli
provenance: source docs/core/interfaces.md
---

# Python CLI orchestration layer

## Answer

The Python CLI orchestration layer is an optional client shell that drives the kernel through public APIs without owning canonical state or persistence semantics.

## Supporting points

- Python is no longer the defining boundary of the architecture; it is one adapter alongside embedded Rust, local IPC, HTTP, or agent-facing protocols.
- It may preserve command continuity and workflow ergonomics, but all authoritative mutations still compile to kernel transaction plans.
- Python should not define identity, revision semantics, hashing, canonicalization, or storage layout.
- Any Python integration should sit behind the same kernel API and capability rules as other clients.

## Related atoms

### Depends on

- [depends_on:: [[kernel-api]]]
- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[ports-and-adapters]]]

### Supports

- [supports:: [[cli-invocation-contract]]]
- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[recover-vs-compose]]]

### Constrains

- [constrains:: [[rust-core]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: core
id: decision-pyo3-ffi
title: Decision embedded FFI is optional, not sovereign
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/core/interfaces.md
---

# Decision embedded FFI is optional, not sovereign

## Answer

An embedded FFI such as PyO3 may exist for Python clients, but it is an adapter choice rather than the defining architecture boundary.

## Supporting points

- The governing public boundary is the kernel API and its transaction/query/projection contracts.
- Embedded FFI is useful for low-overhead local integration, but the same kernel semantics must also support non-Python clients.
- No adapter is allowed to redefine storage, revision, or capability behavior.

## Related atoms

### Supports

- [supports:: [[kernel-api]]]
- [supports:: [[python-cli-orchestration-layer]]]

### Constrains

- [constrains:: [[ports-and-adapters]]]
- [constrains:: [[rust-core]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

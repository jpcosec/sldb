---
layer: shared
id: kernel-api
title: Kernel API
five_wh_one_plus: where
tags:
- system:sldb
- domain:architecture-boundaries
- domain:architecture-integration
provenance: source docs/core/interfaces.md
---

# Kernel API

## Answer

The kernel API is the public authority boundary for opening documents, submitting transactions, running queries, creating projections, and subscribing to kernel events.

## Supporting points

- The same authority surface must be reachable from embedded Rust, Python FFI, local IPC, HTTP, gRPC, UI clients, and agents.
- Public contracts should be typed around document handles, transaction builders, query plans, projection specs, and event streams.
- No client-facing adapter may bypass kernel validation by writing directly to persistence.

## Related atoms

### Depends on

- [depends_on:: [[rust-core]]]
- [depends_on:: [[transaction]]]
- [depends_on:: [[query-engine]]]
- [depends_on:: [[projection]]]

### Supports

- [supports:: [[python-cli-orchestration-layer]]]
- [supports:: [[ports-and-adapters]]]
- [supports:: [[hook-runtime]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: core
id: rust-core
title: Rust core
five_wh_one_plus: what
tags:
- system:sldb
- domain:implementation-rust-core
provenance: source docs/core/core_README.md
---

# Rust core

## Answer

The Rust core is the knowledge kernel that alone enforces canonical data invariants, transactions, revisions, hashing, persistence, and capability-checked effects.

## Supporting points

- Rust is the only authority allowed to produce new revisions.
- Markdown, Lisp, CLI, UI, agents, parsers, and semantic services are projection or adapter surfaces around the kernel rather than alternate authorities.
- The core must stay small enough to verify: types, operations, validation, transaction execution, Merkle hashing, and storage contracts belong here.
- The kernel may expose embedded or daemonized APIs later, but the invariant boundary remains the same.

## Related atoms

### Depends on

- [depends_on:: [[transaction]]]
- [depends_on:: [[revision]]]
- [depends_on:: [[graph-store]]]
- [depends_on:: [[node-hash]]]

### Supports

- [supports:: [[kernel-api]]]
- [supports:: [[query-engine]]]
- [supports:: [[projection]]]
- [supports:: [[projection-surface]]]
- [supports:: [[hook-runtime]]]

### Constrains

- [constrains:: [[ports-and-adapters]]]
- [constrains:: [[lisp-metalanguage]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

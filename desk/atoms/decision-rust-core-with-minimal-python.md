---
layer: core
id: decision-rust-core-with-minimal-python
title: Decision kernel authority stays in Rust
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/core/core_README.md
---

# Decision kernel authority stays in Rust

## Answer

The architecture keeps all authoritative mutation, revision, hashing, persistence, and capability validation inside the Rust kernel. Python, Lisp, CLI, UI, and agents remain clients or metalanguages around that authority.

## Supporting points

- The older Python-orchestration framing is now subordinate to the stronger kernel model.
- Multiple frontends may exist, but none of them may bypass transaction validation or revision production.
- This keeps the smallest correctness-critical surface in one strongly constrained implementation language.

## Related atoms

### Supports

- [supports:: [[rust-core]]]
- [supports:: [[kernel-api]]]
- [supports:: [[lisp-metalanguage]]]

### Constrains

- [constrains:: [[python-cli-orchestration-layer]]]
- [constrains:: [[phase-1-v1-replication]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

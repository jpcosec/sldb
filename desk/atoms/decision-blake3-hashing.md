---
layer: core
id: decision-blake3-hashing
title: Decision blake3 hashing
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/drawer-features/feature-rust-library-stack.md
---

# Decision blake3 hashing

`blake3` is used for cryptographic hashing of nodes and documents (like `SourceHash`). Its extreme performance and intrinsic parallelism make it ideal for rapidly calculating node hashes and building Merkle indexes during workspace rebuilds.

## Related atoms

### Implements
- [implements:: [[node-hash]]]

---
layer: shared
id: reference-behavior
title: Reference behavior
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-testing
provenance: source docs/core/also_core.md
---

# Reference behavior

## Answer

Reference behavior is the normative expected result for a kernel operation, independent of one library stack, host adapter, or storage backend.

## Supporting points

- It is the behavior that conformance cases attest, not one implementation's incidental internals.
- Reference behavior must cover canonical state, revision results, hashes, and rendered outputs where the contract requires them.
- Backends and adapters may vary internally as long as reference behavior stays fixed.

## Related atoms

### Supports

- [supports:: [[conformance-suite]]]
- [supports:: [[decision-rusqlite-store]]]
- [supports:: [[ports-and-adapters]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

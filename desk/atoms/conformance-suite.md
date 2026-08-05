---
layer: shared
id: conformance-suite
title: Conformance suite
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-testing
provenance: source docs/core/also_core.md
---

# Conformance suite

## Answer

A conformance suite is the implementation-independent set of fixtures and expected outcomes that defines kernel behavior across canonicalization, transactions, revisions, hashes, and rendering.

## Supporting points

- It fixes observable behavior independently of Steel, redb, Cozo, Tree-sitter, or other backend choices.
- Each case should bind input, canonical form, transaction result, revision result, hash result, and render result.
- Conformance is the guardrail against architectural drift during implementation swaps.

## Related atoms

### Depends on

- [depends_on:: [[reference-behavior]]]
- [depends_on:: [[golden-fixture]]]

### Supports

- [supports:: [[canonicalizer]]]
- [supports:: [[transaction]]]
- [supports:: [[markdown-emitter]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

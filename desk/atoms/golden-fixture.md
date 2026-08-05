---
layer: shared
id: golden-fixture
title: Golden fixture
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-testing
provenance: source docs/core/plan_core.md
---

# Golden fixture

## Answer

A golden fixture is a pinned input/output artifact set used to prove that canonicalization, hashing, rendering, diffs, or query behavior has not changed unexpectedly.

## Supporting points

- A fixture should include source input plus the expected canonical and rendered outputs relevant to the contract.
- Golden fixtures are especially important for reversible document families and regression-heavy command surfaces.
- Fixture changes are product-truth changes, not incidental test churn.

## Related atoms

### Supports

- [supports:: [[conformance-suite]]]
- [supports:: [[reversible-document-family]]]
- [supports:: [[markdown-roundtrip-contract]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

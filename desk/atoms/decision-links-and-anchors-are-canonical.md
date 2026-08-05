---
layer: shared
id: decision-links-and-anchors-are-canonical
title: "Decision: links and anchors are canonical"
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Decision: links and anchors are canonical

## Answer

Links and anchors are modeled as canonical parts of the target system because they are core addressability and relation primitives, not cosmetic render artifacts.

## Supporting points

- Current and future linking behavior needs stable identity independent of one renderer.
- External anchoring requires explicit canonical payload such as path, hash, sample, and locator data.
- Canonicalizing links and anchors keeps graph projection, inspection, and visual tooling aligned to one truth model.

## Related atoms

### Supports

- [supports:: [[link-edge]]]
- [supports:: [[text-anchor]]]
- [supports:: [[ast-anchor]]]

### Constrains

- [constrains:: [[canonical-address]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

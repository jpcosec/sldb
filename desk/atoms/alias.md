---
layer: shell
id: alias
title: Alias
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-addressability
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Alias

## Answer

An alias is an alternate stable name or selector path that resolves to the same canonical unit.

## Supporting points

- Aliases support resilient access and compatibility surfaces.
- They belong to addressability, not to separate content ownership.
- They are useful for migration and multiple query surfaces.

## Related atoms

### Depends on

- [depends_on:: [[addressability-layer]]]

### Supports

- [supports:: [[stable-selector]]]
- [supports:: [[derived-address]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

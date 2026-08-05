---
layer: shell
id: authorship-state
title: Authorship State
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-provenance
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Authorship State

## Answer

Authorship state distinguishes authored canonical content from derived canonical content.

## Supporting points

- The design requires authored-versus-derived status as a semantic distinction.
- Reversibility, extraction, rendering, and validation behavior depend on this distinction.
- CLI and visual inspection both need to expose whether a value is authored or derived.
## Related atoms

### Depends on

- [depends_on:: [[provenance-record]]]
- [depends_on:: [[field-binding]]]

### Supports

- [supports:: [[draft-first-model-edits]]]
- [supports:: [[projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

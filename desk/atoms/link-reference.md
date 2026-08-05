---
layer: core
id: link-reference
title: Link Reference
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-relations
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Link Reference

## Answer

A link reference is a typed canonical relation from one unit to another target.

## Supporting points

- Links move out of ad hoc string behavior and into explicit canonical structure.
- Link relations need target identity, resolution state, and provenance.
- Graph-friendly navigation and semantic projection depend on links being first-class relations.
## Related atoms

### Depends on

- [depends_on:: [[node]]]
- [depends_on:: [[stable-selector]]]

### Supports

- [supports:: [[recover-vs-compose]]]
- [supports:: [[semantic-export-boundary]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

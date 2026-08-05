---
layer: shell
id: traceability-symmetry
title: Traceability symmetry
five_wh_one_plus: how
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/diagram-traceability-contract.md
---

# Traceability symmetry

## Answer

Traceability between a spec and a view must be declared on both sides: `spec.views` contains a vista iff that vista's `specs` field contains the spec.

## Supporting points

- One-sided declarations detect the two classic omissions: a new spec nobody diagrammed, and a new diagram nobody registered.
- Symmetry is mechanically checkable, so the rule is enforced by validator rather than by review discipline.
- The same rule binds vista ↔ puml as a 1:1 mapping declared in the registry.

## Related atoms

### Supports

- [supports:: [[specyaml-nexus]]]
- [supports:: [[coverage-warning]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

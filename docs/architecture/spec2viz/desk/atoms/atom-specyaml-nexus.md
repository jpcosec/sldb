---
layer: shell
id: specyaml-nexus
title: SpecYAML nexus
five_wh_one_plus: what
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/specyaml-schema-contract.md
---

# SpecYAML nexus

## Answer

SpecYAML (`docs/architecture/spec2viz/`) is the machine-readable nexus between knowledge atoms and diagram projections: atoms govern it, and diagrams are derived from it.

## Supporting points

- It declares what exists (nodes, edges, containment) and how it connects, in a form scripts can validate.
- Its only sanctioned edge into the atom layer is the `atoms:` reference field; its only edge into views is the symmetric `views:` field.
- It is a candidate `StructuredNLDoc` family once the kernel store exists: model, validation, and projections are already its shape.

## Related atoms

### Depends on

- [depends_on:: [[atom-reference-edge]]]
- [depends_on:: [[traceability-symmetry]]]

### Supports

- [supports:: [[diagram-as-projection]]]
- [supports:: [[structurednldoc-contract]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

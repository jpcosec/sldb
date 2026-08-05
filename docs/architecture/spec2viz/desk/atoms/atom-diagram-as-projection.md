---
layer: shell
id: diagram-as-projection
title: Diagram as projection
five_wh_one_plus: why
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/diagram-traceability-contract.md
---

# Diagram as projection

## Answer

A diagram is a projection of upstream truth (atoms and specyaml), never a document of record: it is derived, registered, and reconstructible.

## Supporting points

- Editing a diagram without touching its source breaks the chain; editing flows upstream-to-downstream only.
- A diagram element without a spec entry is a validation error; a spec node without any view is a coverage signal.
- This mirrors the kernel's own principle that derived state is rebuildable from canonical state.

## Related atoms

### Depends on

- [depends_on:: [[specyaml-nexus]]]
- [depends_on:: [[graph-projection]]]

### Supports

- [supports:: [[generated-artifact-drift]]]
- [supports:: [[coverage-warning]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

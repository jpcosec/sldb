---
layer: core
id: decision-relation-ast-extensibility
title: "Decision: relation AST extensibility"
five_wh_one_plus: why
tags:
- system:sldb
- domain:architecture-decisions
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Decision: relation AST extensibility

## Answer

Relations carry extensible relation-AST payloads because thin fixed edges would make the graph model too rigid for evolving link semantics, store semantics, provenance, and future plugin behavior.

## Supporting points

- The target ontology treats relations as first-class structures, not just anonymous connectors.
- Extensible relation payloads reduce pressure to bloat the base node schema.
- This keeps the graph-native substrate open to richer behaviors without rewriting the whole persistence model.

## Related atoms

### Supports

- [supports:: [[relation-ast]]]
- [supports:: [[link-edge]]]
- [supports:: [[store-edge]]]

### Constrains

- [constrains:: [[graph-store]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

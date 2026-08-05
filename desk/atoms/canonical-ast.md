---
layer: core
id: canonical-ast
title: Canonical AST
five_wh_one_plus: what
tags:
- system:sldb
- domain:model-ast-core
provenance: source docs/drawer-features/feature-sldb-explicit-target-architecture.md
---

# Canonical AST

## Answer

The canonical AST is the structural source of truth for authored document families and a shared substrate inside the refactored kernel's canonical graph/revision model.

## Supporting points

- Markdown is an importer/exporter and editing surface rather than the sovereign representation.
- CLI workflows, future visual UX, importers, emitters, and infrastructure depend on this structural substrate.
- Documents, revisions, nodes, edges, transactions, and provenance remain canonical kernel concerns.
- Store behavior is not an alternate authority; it persists canonical kernel state, including structural AST data where applicable.

## Related atoms

### Supports

- [supports:: [[rust-patterns]]]
- [supports:: [[rust-testing]]]

### Constrains

- [constrains:: [[rust-code-linting]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Supports
- [supports:: [[reversible-document-family]]]

---
layer: shell
id: python-patterns
title: Python patterns
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-patterns-python
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Python patterns

## Answer

Python patterns define the reusable implementation shapes for CLI orchestration, model-facing workflows, migration layers, and user-facing tooling around the canonical core.

## Supporting points

- Python should preserve the recognizable SLDB CLI and workflow ergonomics.
- Patterns here should favor thin orchestration, explicit contracts, low duplication, and clear boundaries around the Rust core.
- These patterns should keep user behavior stable while internals evolve.

## Related atoms

### Depends on

- [depends_on:: [[patterns]]]
- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[structurednldoc-contract]]]

### Supports

- [supports:: [[code-linting]]]
- [supports:: [[testing]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

### Supports
- [supports:: [[direct-mode-vs-store-backed-mode]]]

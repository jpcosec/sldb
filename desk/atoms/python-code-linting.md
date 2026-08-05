---
layer: shell
id: python-code-linting
title: Python code linting
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-clean-code-python
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# Python code linting

## Answer

Python code linting keeps the CLI and orchestration layers readable, unsurprising, and aligned with the target architecture.

## Supporting points

- It should reduce command-surface clutter, routing sprawl, duplicated helpers, and hidden workflow logic.
- It should preserve a clean user-facing shell over the deeper core refactor.
- It is a clean-code dimension specialized for the Python surfaces.

## Related atoms

### Depends on

- [depends_on:: [[code-linting]]]
- [depends_on:: [[python-patterns]]]

### Constrains

- [constrains:: [[cli-workflow-surface]]]
- [constrains:: [[plural-first-cli-surface-and-legacy-alias-status]]]
- [constrains:: [[create-vs-track-vs-update]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

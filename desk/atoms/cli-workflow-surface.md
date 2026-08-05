---
layer: shell
id: cli-workflow-surface
title: CLI Workflow Surface
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/drawer-features/feature-sldb-product-principles-and-cli-continuity.md
---

# CLI Workflow Surface

## Answer

The CLI workflow surface is the terminal-facing operating surface that must remain recognizable across the refactor.

## Supporting points

- CLI continuity is an explicit product constraint even while internals change deeply.
- The recognizable SLDB command family should survive with reduced clutter and cleaner implementation.
- The CLI is a consumer of the canonical substrate rather than an independent truth source.

## Related atoms

### Supports

- [supports:: [[python-patterns]]]
- [supports:: [[python-testing]]]

### Constrains

- [constrains:: [[python-code-linting]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

---
layer: shared
id: model-reference-format
title: Model reference format
five_wh_one_plus: how
tags:
- system:sldb
- domain:surfaces-cli-inputs-outputs
provenance: source docs/sldb-v1/README.md
---

# Model reference format

## Answer

Model identifiers are Python import refs in `module:ClassName` form, not raw file paths; pass `--pythonpath` when needed to make the module importable.

## Supporting points

- This is the public contract for model addressing in the CLI.
- It keeps model resolution stable across commands.
- The refactor should preserve this recognizable model reference pattern.
## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]

### Supports

- [supports:: [[structurednldoc-contract]]]
- [supports:: [[draft-first-model-edits]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

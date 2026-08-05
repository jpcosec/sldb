---
layer: shell
id: models-command-group
title: models command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `models` command group

## Answer

The `models` command group is the CLI surface for registering, inspecting, editing, validating, and promoting typed document-model contracts.

## Supporting points

- It is the public surface for model lifecycle management.
- It exposes the StructuredNLDoc contract operationally.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[structurednldoc-contract]]]

### Supports

- [supports:: [[model-reference-format]]]
- [supports:: [[field-descriptions-are-required-contract]]]
- [supports:: [[draft-first-model-edits]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

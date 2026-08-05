---
layer: shell
id: sections-command-group
title: sections command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `sections` command group

## Answer

The `sections` command group is the CLI surface for inspecting and querying section-level document structure and ownership.

## Supporting points

- It exposes deeper structural navigation than whole-document access.
- It depends on section indexing and tree-aware canonical structure.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[section-index]]]
- [depends_on:: [[tree-spine]]]

### Supports

- [supports:: [[field-and-section-navigation]]]
- [supports:: [[semantic-vs-physical-search]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

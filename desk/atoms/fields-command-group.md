---
layer: shell
id: fields-command-group
title: fields command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `fields` command group

## Answer

The `fields` command group is the CLI surface for inspecting, querying, updating, appending, and cleaning field-level document state.

## Supporting points

- It exposes field-aware operations as first-class user workflows.
- It depends on explicit field binding and field indexing.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[field-binding]]]
- [depends_on:: [[field-index]]]

### Supports

- [supports:: [[field-and-section-navigation]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

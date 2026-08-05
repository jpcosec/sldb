---
layer: shell
id: stores-command-group
title: stores command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `stores` command group

## Answer

The `stores` command group is the CLI surface for initializing, inspecting, checking, updating, and exporting store-backed SLDB metadata workspaces.

## Supporting points

- It owns store lifecycle and maintenance behavior at the CLI surface.
- It is user-facing orchestration over store infrastructure rather than canonical content itself.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[store-infrastructure]]]

### Supports

- [supports:: [[what-a-store-is]]]
- [supports:: [[store-integrity-checks]]]
- [supports:: [[semantic-export-boundary]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

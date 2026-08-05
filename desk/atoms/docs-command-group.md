---
layer: shell
id: docs-command-group
title: docs command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `docs` command group

## Answer

The `docs` command group is the CLI surface for creating, tracking, updating, recovering, composing, and showing document-level SLDB workflows.

## Supporting points

- It is the operational document lifecycle surface for users.
- It connects payload workflows with tracked-document behavior.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[document-tracker]]]
- [depends_on:: [[document-materializer]]]

### Supports

- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[recover-vs-compose]]]
- [supports:: [[tracked-document-identity]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

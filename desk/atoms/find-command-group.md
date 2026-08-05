---
layer: shell
id: find-command-group
title: find command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-command-groups
provenance: source docs/sldb-v1/README.md
---

# `find` command group

## Answer

The `find` command group is the CLI retrieval surface for physical and semantic search over store-backed SLDB knowledge.

## Supporting points

- It is the primary discovery surface for users.
- It depends on search projections and query execution.
- It is part of the plural-first primary interface.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]
- [depends_on:: [[query-engine]]]
- [depends_on:: [[search-projection]]]

### Supports

- [supports:: [[semantic-vs-physical-search]]]
- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

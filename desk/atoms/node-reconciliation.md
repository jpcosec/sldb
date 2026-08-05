---
layer: shell
id: node-reconciliation
title: Node reconciliation
five_wh_one_plus: how
tags:
- system:sldb
- domain:pipeline-importers
provenance: source docs/core/also_core.md
---

# Node reconciliation

## Answer

Node reconciliation is the process that matches external-source changes against canonical identity rules and compiles the result into primitive operations instead of blindly replacing whole documents.

## Supporting points

- It decides whether a unit is unchanged, modified, moved, removed, or recreated.
- Reconciliation must preserve identity where the rules permit it and mint new identity where they do not.
- The output of reconciliation is a transaction-shaped change set, not ad hoc source patching.

## Related atoms

### Depends on

- [depends_on:: [[identity-stability-rules]]]
- [depends_on:: [[source-manager]]]
- [depends_on:: [[primitive-operation]]]

### Supports

- [supports:: [[update-tracked-document-workflow]]]
- [supports:: [[anchor-comment]]]
- [supports:: [[tracked-document-identity]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

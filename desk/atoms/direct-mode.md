---
layer: shell
id: direct-mode
title: Direct mode
five_wh_one_plus: when
tags:
- system:sldb
- domain:surfaces-cli-workflows
provenance: source docs/sldb-v1/faq.md
---

# Direct mode

## Answer

Use direct mode when a command can operate on models, payloads, or documents without depending on store registrations or project indexes.

## Supporting points

- It fits extract, render, and validate style workflows.
- It avoids requiring `.sldb/` for every operation.
- It remains an important lightweight operating mode.

## Related atoms

### Contrasts with

- [contrasts_with:: [[store-backed-mode]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

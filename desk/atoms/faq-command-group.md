---
layer: shell
id: faq-command-group
title: faq command group
five_wh_one_plus: where
tags:
- system:sldb
- domain:surfaces-cli-onboarding
provenance: source docs/sldb-v1/faq.md
---

# `faq` command group

## Answer

The `faq` command group is the CLI onboarding surface that answers first-use contract questions about stores, models, docs, search, and tracking.

## Supporting points

- It is a behavior-discovery surface rather than a core runtime component.
- It externalizes stable user-facing definitions from the docs.
- It supports adoption and contract clarity.

## Related atoms

### Depends on

- [depends_on:: [[cli-workflow-surface]]]

### Supports

- [supports:: [[what-a-store-is]]]
- [supports:: [[structurednldoc-contract]]]
- [supports:: [[tracked-document-identity]]]
- [supports:: [[semantic-vs-physical-search]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

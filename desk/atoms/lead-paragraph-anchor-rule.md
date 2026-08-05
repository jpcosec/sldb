---
layer: shared
id: lead-paragraph-anchor-rule
title: Lead paragraph anchor rule
five_wh_one_plus: how
tags:
- system:sldb
- domain:model-text-structure
provenance: source docs/sldb-v1/docs-README.md
---

# Lead paragraph anchor rule

## Answer

When using generic `title + body`, keep a short paragraph after the H1 before dense fenced blocks or subsections so extraction stays stable.

## Supporting points

- This is a documented authoring pattern for extraction stability.
- It is user-facing guidance tied to expected behavior.
- It should remain valid unless the extraction contract changes materially.
## Related atoms

### Depends on

- [depends_on:: [[structurednldoc-contract]]]

### Supports

- [supports:: [[shallow-title-plus-body-default]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

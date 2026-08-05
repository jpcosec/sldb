---
layer: shell
id: python-testing
title: Python testing
five_wh_one_plus: how
tags:
- system:sldb
- domain:quality-testing-python
provenance: source docs/architecture/ritual-testing.md
---

# Python testing

## Answer

Python testing validates the observable behavior of CLI workflows, model operations, and user-facing orchestration around the canonical core.

## Supporting points

- It should cover command behavior, payload flows, tracked-document workflows, and regression of the recognizable SLDB experience.
- It should include both unit and UX-oriented CLI behavior checks.
- It proves that the refactor preserves the product contract at the user surface.

## Related atoms

### Depends on

- [depends_on:: [[testing]]]
- [depends_on:: [[python-patterns]]]
- [depends_on:: [[cli-workflow-surface]]]

### Supports

- [supports:: [[cli-invocation-contract]]]
- [supports:: [[create-vs-track-vs-update]]]
- [supports:: [[recover-vs-compose]]]
- [supports:: [[semantic-vs-physical-search]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

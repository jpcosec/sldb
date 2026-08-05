---
layer: shell
id: coverage-warning
title: Coverage warning
five_wh_one_plus: how
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/diagram-traceability-contract.md
---

# Coverage warning

## Answer

A coverage warning surfaces a legitimate gap in the traceability graph: a spec with no view, or a view with no spec. It is reported, not fatal.

## Supporting points

- Warnings make the documentation backlog explicit and machine-listable instead of implicit.
- Errors mean the chain is broken; warnings mean the chain is incomplete. The distinction keeps CI green while keeping gaps visible.
- Closing a warning is a deliberate planning act: write the missing spec or register the missing view.

## Related atoms

### Depends on

- [depends_on:: [[traceability-symmetry]]]
- [depends_on:: [[diagram-as-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

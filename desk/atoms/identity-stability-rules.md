---
layer: core
id: identity-stability-rules
title: Identity stability rules
five_wh_one_plus: how
tags:
- system:sldb
- domain:model-identity
provenance: source docs/core/also_core.md
---

# Identity stability rules

## Answer

Identity stability rules define when a canonical unit keeps its identity, receives a new identity, counts as moved, or counts as deleted and recreated.

## Supporting points

- These rules govern node continuity across edits, imports, reconciliation, anchoring, and projections.
- Stable identity must not collapse into one parser's positions or one adapter's handles.
- Reconciliation quality depends on making identity stability explicit rather than heuristic-only.

## Related atoms

### Depends on

- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[tracked-document-identity]]]

### Supports

- [supports:: [[node-reconciliation]]]
- [supports:: [[stable-selector]]]
- [supports:: [[provenance-record]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

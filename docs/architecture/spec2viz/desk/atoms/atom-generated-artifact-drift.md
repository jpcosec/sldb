---
layer: shell
id: generated-artifact-drift
title: Generated artifact drift
five_wh_one_plus: how
tags:
- system:sldb
- domain:documentation-traceability
provenance: docs/architecture/contracts/diagram-traceability-contract.md
---

# Generated artifact drift

## Answer

A generated artifact must regenerate byte-identical from its declared sources; any difference is drift and fails validation.

## Supporting points

- Hand edits to generated artifacts are forbidden because they are undetectable without a regeneration check.
- Drift checking turns "remember to regenerate" into a CI gate: committed output must equal regenerated output.
- Tooling layers (annotation data, browser state) must live outside the artifact or in its template so they survive regeneration.

## Related atoms

### Depends on

- [depends_on:: [[diagram-as-projection]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

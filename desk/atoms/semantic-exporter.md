---
layer: core
id: semantic-exporter
title: Semantic exporter
five_wh_one_plus: how
tags:
- system:sldb
- domain:runtime-projections
provenance: source docs/sldb-v1/README.md
---

# Semantic exporter

## Answer

The semantic exporter emits SLDB-owned semantic document truth for downstream graph or semantic consumers without taking ownership of their downstream edges.

## Supporting points

- It is the operational component behind the semantic export boundary.
- It should export canonical-derived semantics plus provenance.
- It should not absorb downstream workflow-specific semantics.

## Related atoms

### Depends on

- [depends_on:: [[semantic-export-boundary]]]
- [depends_on:: [[graph-projection]]]

### Supports

- [supports:: [[how-to-get-data-out-of-sldb]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

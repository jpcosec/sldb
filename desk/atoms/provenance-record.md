---
layer: shared
id: provenance-record
title: Provenance Record
five_wh_one_plus: what
tags:
- system:sldb
- domain:runtime-provenance
provenance: source docs/drawer-features/feature-canonical-ast-design-current-state.md
---

# Provenance Record

## Answer

A provenance record captures where canonical data came from and how it changed over time.

## Supporting points

- The target architecture requires lineage beyond git-only history.
- Provenance must connect nodes and fields to import sources and transformations.
- Canonical history needs explicit timestamps, revision knowledge, and evidence-bearing change records.
## Related atoms

### Depends on

- [depends_on:: [[canonical-identity]]]
- [depends_on:: [[node]]]

### Supports

- [supports:: [[authorship-state]]]
- [supports:: [[node-hash]]]
- [supports:: [[semantic-export-boundary]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

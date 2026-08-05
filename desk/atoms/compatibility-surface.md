---
layer: shared
id: compatibility-surface
title: Compatibility surface
five_wh_one_plus: what
tags:
- system:sldb
- domain:architecture-migration-strategy
provenance: source docs/core/also_core.md
---

# Compatibility surface

## Answer

A compatibility surface is the versioned contract that must remain intelligible across kernel evolution for persistence, canonical model, operations, protocols, schemas, projections, or plugins.

## Supporting points

- Compatibility should be versioned by surface, not assumed to share one global version.
- Persisted format, canonical model, operation semantics, and external protocols may evolve at different rates.
- Compatibility commitments define when migration is required and what kinds of mixed-version interaction are allowed.

## Related atoms

### Supports

- [supports:: [[migration-unit]]]
- [supports:: [[legacy-cli-aliases]]]
- [supports:: [[decision-v1-parity-before-scope-expansion]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

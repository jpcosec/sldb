---
layer: shared
id: observability-surface
title: Observability surface
five_wh_one_plus: what
tags:
- system:sldb
- domain:quality-reliability
provenance: source docs/core/also_core.md
---

# Observability surface

## Answer

The observability surface is the set of logs, traces, metrics, explanations, and status signals that let users and tools understand what the kernel did and why.

## Supporting points

- Observability should cover transactions, invalidations, hashes, projections, queries, effects, agents, and degraded states.
- Explainability is part of the runtime contract, not just debug convenience.
- Observability data must preserve provenance and avoid becoming an alternate mutable source of truth.

## Related atoms

### Supports

- [supports:: [[transaction-log]]]
- [supports:: [[degraded-mode]]]
- [supports:: [[hook-runtime]]]

### 5WH1+ neighborhood

- This atom is typed by its `five_wh_one_plus` field and should be queried together with nearby `what`/`how`/`when`/`where` atoms rather than as an isolated note.

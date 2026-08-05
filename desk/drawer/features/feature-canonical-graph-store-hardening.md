---
id: feature-canonical-graph-store-hardening
status: proposed
summary: Harden canonical graph-store integrity, verification, recovery, corruption handling, and degraded-mode behavior beyond the first slice.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- also_core.md
- core_README.md
- libraries_core.md
- desk/atoms/graph-store.md
- desk/atoms/store-recovery.md
- desk/atoms/corruption-state.md
- desk/atoms/degraded-mode.md
- desk/atoms/failure-model.md
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Canonical graph-store hardening

## Goal

Define the macrotask for store verification, recovery, corruption handling, and degraded operation once the first-slice kernel/store foundation exists.

## Includes

- verify/rebuild flows
- corruption detection and classification
- degraded-mode behavior
- operator-visible recovery controls
- store-usable vs store-needs-recovery boundary

## Excludes

- semantic indexing rollout
- product-surface scope expansion unrelated to store integrity

## Needs design or grounding before promotion

- exact verify command surface
- exact rebuild scope for caches, projections, and indexes
- exact corruption-state classification
- exact operator recovery sequence

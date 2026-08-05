---
id: feature-post-phase-1-scope-expansion
status: proposed
summary: Gather all explicitly deferred work after Phase 1, including embeddings, broader families, richer projections, and expanded product surfaces.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as roadmap-expansion planning feature."
references:
- plan_core.md
- libraries_core.md
- docs/architecture/contracts/phase-1-parity-contract.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-phase-1-closure-package
---

# Post Phase 1 scope expansion

## Goal

Define the expansion bucket after the first committed product closure is complete.

## Includes

- embeddings and semantic indexing
- broader document-family support
- richer projections/materializations
- deferred agent/UI expansions

## Excludes

- backporting scope creep into Phase 1
- treating deferred work as implicitly approved for the first slice

## Needs design or grounding before promotion

- expansion ordering
- dependency structure across deferred features
- which deferred surfaces become Phase 2 vs later
- acceptance packaging for post-Phase-1 work

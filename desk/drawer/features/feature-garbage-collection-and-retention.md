---
id: feature-garbage-collection-and-retention
status: proposed
summary: Define retention roots, pinning, pruning, and garbage-collection policy for canonical and derived artifacts.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- core_README.md
- plan_core.md
- desk/atoms/garbage-collection.md
- desk/atoms/retention-policy.md
- desk/atoms/backup-export.md
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Garbage collection and retention

## Goal

Define the macrotask for keeping what must persist, pruning what may be rebuilt, and protecting pinned history correctly.

## Includes

- retention roots and pins
- GC policy
- pruning rules for payloads, caches, projections, and indexes
- safety rules around canonical history

## Excludes

- backup/import behavior beyond retention interaction
- semantic-provider rollout

## Needs design or grounding before promotion

- canonical reachability rules
- what may be pruned vs must be retained
- scheduling and operator controls
- attestation for safe pruning

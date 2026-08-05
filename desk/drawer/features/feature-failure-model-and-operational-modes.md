---
id: feature-failure-model-and-operational-modes
status: proposed
summary: Define failure classes, degraded modes, recovery states, and operator-visible operational transitions across the product.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as cross-cutting macrotask planning feature."
references:
- also_core.md
- libraries_core.md
- desk/atoms/failure-model.md
- desk/atoms/degraded-mode.md
- desk/atoms/corruption-state.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-canonical-graph-store-hardening
---

# Failure model and operational modes

## Goal

Define the macrotask for classifying failures and making degraded/recovery states explicit rather than implicit.

## Includes

- failure classes
- degraded modes
- recovery states
- operator-visible transitions and limits

## Excludes

- hand-wavy generic error handling
- semantic retrieval scope expansion

## Needs design or grounding before promotion

- exact failure taxonomy
- state machine for degraded/recovery modes
- user-visible behavior in each mode
- attestation of safe fallback behavior

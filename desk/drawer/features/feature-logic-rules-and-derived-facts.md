---
id: feature-logic-rules-and-derived-facts
status: proposed
summary: Define rule evaluation, logical derivation, and materialized fact surfaces over canonical state.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- also_core.md
- libraries_core.md
- desk/atoms/logic-engine.md
- desk/atoms/projection.md
- desk/atoms/reference-behavior.md
- docs/architecture/spec2viz/target-components.yml
depends_on:
- feature-specialized-projection-surfaces
---

# Logic rules and derived facts

## Goal

Define the macrotask for rule-based derivation and materialized logical facts over canonical content.

## Includes

- rule evaluation
- derived fact materialization
- invalidation/rebuild policy
- operator-visible provenance of derived facts

## Excludes

- authority reassignment to logic outputs
- opaque hidden inference paths

## Needs design or grounding before promotion

- rule language boundary
- provenance model for derived facts
- rebuild vs incremental update strategy
- explainability for logical conclusions

---
id: feature-observability-and-diagnostics
status: proposed
summary: Define traces, diagnostics, explain/status surfaces, and operator visibility across kernel, queries, projections, and effects.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as cross-cutting macrotask planning feature."
references:
- also_core.md
- libraries_core.md
- desk/atoms/observability-surface.md
- desk/atoms/query-plan.md
- desk/atoms/effect-plan.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-store-graph.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Observability and diagnostics

## Goal

Define the macrotask for making system behavior inspectable by operators and product surfaces.

## Includes

- runtime traces
- status/explain outputs
- query/effect diagnostics
- stored observability artifacts where appropriate

## Excludes

- observability that silently changes authority
- UI-only assumptions

## Needs design or grounding before promotion

- exact status/explain surface
- retention policy for traces/logs
- redaction/privacy boundaries
- operator workflows for diagnosis

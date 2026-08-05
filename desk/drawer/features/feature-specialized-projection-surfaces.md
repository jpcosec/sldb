---
id: feature-specialized-projection-surfaces
status: proposed
summary: Define specialized projection surfaces such as semantic graph views, dependency trees, anchor maps, task views, and agent subgraphs.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- diagramas_core.md
- plan_core.md
- desk/atoms/projection.md
- desk/atoms/projection-surface.md
- desk/atoms/search-projection.md
- docs/architecture/spec2viz/target-components.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Specialized projection surfaces

## Goal

Define the macrotask for structured derived views over canonical state for focused product and operator use cases.

## Includes

- semantic graph views
- dependency trees
- task views
- anchor maps
- agent subgraphs

## Excludes

- generic renders/materializations
- authority reassignment away from canonical state

## Needs design or grounding before promotion

- projection catalog and naming
- cacheability/rebuild policy
- capability boundaries per projection
- explainability for projected views

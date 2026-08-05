---
id: feature-desktop-or-visual-ui-surface
status: proposed
summary: Define whether and how a desktop or visual UI surface should expose canonical state, renders, and projections.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as deferred product-surface planning feature."
references:
- diagramas_core.md
- interfaces.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-cli-surface-implementation
---

# Desktop or visual UI surface

## Goal

Define the deferred macrotask for a visual product surface, if it remains in target scope.

## Includes

- visual inspection surface
- graph/document/task views
- render/projection presentation policy

## Excludes

- assuming UI is required before CLI maturity
- bypassing kernel authority

## Needs design or grounding before promotion

- whether UI remains in committed scope
- minimal visual surface worth building
- edit vs inspect boundary
- projection/render choices per view

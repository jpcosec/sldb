---
id: feature-agent-and-mcp-surface
status: proposed
summary: Define agent-facing and MCP-facing product surfaces over canonical state, projections, and controlled actions.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- interfaces.md
- plan_core.md
- desk/atoms/capability-model.md
- desk/atoms/projection-surface.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-cli-surface-implementation
---

# Agent and MCP surface

## Goal

Define the macrotask for controlled agent-facing access to canonical state, projections, and approved action surfaces.

## Includes

- agent harness boundary
- MCP/client contract
- subgraph/task-oriented derived views
- capability-gated action surface

## Excludes

- unconstrained autonomous mutation
- hidden authority channels outside the kernel

## Needs design or grounding before promotion

- exact read/write capability split
- MCP surface shape
- task/subgraph projection policy for agents
- attestation for agent-visible outputs

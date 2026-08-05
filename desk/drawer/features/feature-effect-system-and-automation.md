---
id: feature-effect-system-and-automation
status: proposed
summary: Define effect plans, outbox behavior, runners, hooks, and capability-controlled automation around canonical state changes.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- interfaces.md
- libraries_core.md
- desk/atoms/effect-plan.md
- desk/atoms/hook-runtime.md
- desk/atoms/capability-model.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-lisp-control-and-data-surface-first-slice
---

# Effect system and automation

## Goal

Define the macrotask for controlled effects and hook-driven automation without creating hidden authority paths.

## Includes

- effect plans
- outbox and runner model
- hook triggers
- capability-gated external actions
- observability of effect execution

## Excludes

- unrestricted plugin execution
- bypass of transaction/capability controls

## Needs design or grounding before promotion

- exact effect boundary
- retry/failure model for effects
- sandbox policy
- operator approval or attestation model for risky actions

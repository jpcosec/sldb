---
id: feature-query-language-and-explainability
status: proposed
summary: Define the query surface, plan/explain behavior, and operator-visible inspection tools over canonical state and derived views.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- interfaces.md
- plan_core.md
- desk/atoms/query-plan.md
- desk/atoms/query-engine.md
- desk/atoms/explainability.md
- docs/architecture/spec2viz/target-components.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
- feature-lisp-control-and-data-surface-first-slice
---

# Query language and explainability

## Goal

Define the macrotask for query authoring, plan visibility, explain surfaces, and inspection/debug UX over canonical state.

## Includes

- query surface contract
- explain/debug outputs
- plan inspection
- operator-visible query reasoning

## Excludes

- embeddings-first retrieval
- unrelated GUI work

## Needs design or grounding before promotion

- exact first nontrivial query language surface
- explain output shape
- query safety/capability policy
- how lexical vs structural vs semantic retrieval are separated

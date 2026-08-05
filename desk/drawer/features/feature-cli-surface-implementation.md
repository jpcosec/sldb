---
id: feature-cli-surface-implementation
status: proposed
summary: Implement the actual CLI command-group product surface over the approved kernel, Lisp, and Markdown contracts.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as product-surface macrotask planning feature."
references:
- interfaces.md
- desk/atoms/cli-workflow-surface.md
- desk/atoms/plural-first-cli-surface.md
- docs/architecture/contracts/cli-parity-contract.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
- feature-lisp-control-and-data-surface-first-slice
- feature-markdown-roundtrip-first-slice
---

# CLI surface implementation

## Goal

Define the macrotask for the actual user-facing CLI product surface over the first approved implementation layers.

## Includes

- command-group behavior
- output formats
- direct vs store-backed mode behavior
- help/error/explain UX

## Excludes

- GUI surfaces
- semantic-provider expansion unless separately promoted

## Needs design or grounding before promotion

- promotion order of command groups
- exact first usable CLI subset
- operator diagnostics in CLI form
- acceptance fixtures per command family

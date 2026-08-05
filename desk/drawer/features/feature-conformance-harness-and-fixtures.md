---
id: feature-conformance-harness-and-fixtures
status: proposed
summary: Define the behavioral attestation harness, fixture corpus, and reference behavior needed to prove product contracts across slices.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as cross-cutting macrotask planning feature."
references:
- core_README.md
- plan_core.md
- desk/atoms/conformance-suite.md
- desk/atoms/golden-fixture.md
- desk/atoms/reference-behavior.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-runtime.yml
depends_on:
- feature-rust-kernel-foundation-first-slice
---

# Conformance harness and fixtures

## Goal

Define the macrotask for proving product behavior with fixtures and reference expectations rather than informal confidence.

## Includes

- conformance suite shape
- golden fixtures
- reference behavior policy
- attestation boundaries per feature slice

## Excludes

- vague manual-only validation
- implementation claims without fixture proof

## Needs design or grounding before promotion

- fixture organization
- attestation granularity per subsystem
- cross-surface conformance policy
- reference behavior source hierarchy

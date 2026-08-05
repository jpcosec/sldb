---
id: feature-node-identity-and-reconciliation
status: proposed
summary: Define stable node identity, reconciliation rules, and canonicalization conflict handling across authored inputs and revisions.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- also_core.md
- core_README.md
- desk/atoms/node-reconciliation.md
- desk/atoms/identity-stability-rules.md
- desk/atoms/canonical-ast.md
- docs/architecture/target-system-overview.md
depends_on:
- feature-rust-kernel-foundation-first-slice
- feature-markdown-roundtrip-first-slice
---

# Node identity and reconciliation

## Goal

Define the macrotask for stable node identity and deterministic reconciliation across repeated imports, edits, and canonical rewrites.

## Includes

- stable identity rules
- reconciliation policy
- merge/update semantics
- canonicalization conflict handling

## Excludes

- distributed collaboration policy
- semantic-provider expansion

## Needs design or grounding before promotion

- exact identity inputs
- duplicate vs same-entity rules
- reconciliation precedence across surfaces
- fixtures for identity stability across edits

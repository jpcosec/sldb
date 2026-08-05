---
id: feature-multi-family-document-support
status: proposed
summary: Expand beyond the initial Markdown family into additional authored/imported document families with canonicalization and materialization contracts.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- also_core.md
- interfaces.md
- plan_core.md
- desk/atoms/reversible-document-family.md
- desk/atoms/document-family.md
- desk/atoms/markdown-importer.md
- docs/architecture/spec2viz/target-anchoring.yml
depends_on:
- feature-markdown-roundtrip-first-slice
---

# Multi-family document support

## Goal

Define the macrotask for expanding canonical import/materialization support beyond the first Markdown reversible family.

## Includes

- new family boundaries
- family-specific locator rules
- canonicalization contracts per family
- materialization/export expectations per family

## Excludes

- uncontrolled family sprawl
- semantic retrieval scope creep disguised as family support

## Needs design or grounding before promotion

- family rollout order
- reversible vs lossy family policy
- per-family acceptance bars
- shared vs family-specific anchor behavior

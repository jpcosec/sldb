---
id: feature-anchoring-and-selector-stability
status: proposed
summary: Define stable anchoring, selector behavior, and anchor payload guarantees across import, revision, and render flows.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- diagramas_core.md
- interfaces.md
- desk/atoms/anchor.md
- desk/atoms/selector.md
- desk/atoms/identity-stability-rules.md
- docs/architecture/spec2viz/target-anchoring.yml
depends_on:
- feature-markdown-roundtrip-first-slice
---

# Anchoring and selector stability

## Goal

Define the macrotask for stable anchor identity and selector semantics across canonical revisions and surface materializations.

## Includes

- anchor payload rules
- selector stability rules
- source hash and locator behavior
- family-specific locator boundaries

## Excludes

- unrelated semantic search work
- broad new document-family rollout unless needed for selector rules

## Needs design or grounding before promotion

- exact selector precedence
- exact relocation/rebind behavior
- failure modes for stale anchors
- attestation fixtures for anchor stability

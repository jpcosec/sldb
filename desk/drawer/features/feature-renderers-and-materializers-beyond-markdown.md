---
id: feature-renderers-and-materializers-beyond-markdown
status: proposed
summary: Define render/materialization surfaces beyond Markdown, including HTML, JSON, S-expression, and API payload outputs.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted as post-first-slice macrotask planning feature."
references:
- core_README.md
- interfaces.md
- desk/atoms/document-materializer.md
- desk/atoms/markdown-emitter.md
- desk/atoms/projection-surface.md
- docs/architecture/spec2viz/target-components.yml
depends_on:
- feature-markdown-roundtrip-first-slice
---

# Renderers and materializers beyond Markdown

## Goal

Define the macrotask for canonical output surfaces beyond the first Markdown materialization.

## Includes

- HTML output
- JSON output
- S-expression output
- API payload materialization contracts

## Excludes

- treating renders as authority
- semantic-provider rollout unless needed by a specific output

## Needs design or grounding before promotion

- output ordering and fidelity guarantees
- which outputs are normative vs convenience surfaces
- shared renderer registry rules
- conformance fixtures per output type

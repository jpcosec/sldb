---
id: feature-prosemirror-editor-surface
status: proposed
summary: Define a ProseMirror-backed editor surface that maps authored editor state and selections to kernel-controlled canonical state and materializations.
tags:
- workspace:desk
- artifact:feature
- system:sldb
history:
- "2026-07-29: drafted to capture the discussed editor surface explicitly."
references:
- interfaces.md
- libraries_core.md
- desk/atoms/markdown-text-surface.md
- desk/atoms/selector.md
- desk/atoms/anchor.md
- docs/architecture/spec2viz/target-components.yml
- docs/architecture/spec2viz/target-anchoring.yml
depends_on:
- feature-anchoring-and-selector-stability
- feature-node-identity-and-reconciliation
- feature-multi-family-document-support
---

# ProseMirror editor surface

## Goal

Define the macrotask for a ProseMirror-backed authored editor surface that remains subordinate to kernel-owned canonical state.

## Includes

- editor-state import/export boundary
- mapping between editor selections and canonical anchors/selectors
- transaction path from editor edits into kernel-controlled updates
- materialization policy from canonical state back into editor-consumable structure

## Excludes

- treating editor state as canonical authority
- assuming editor transactions bypass kernel validation

## Must stay true

- editor state is authored input or rendered materialization, not authority
- canonical meaning and revision truth stay in the Rust kernel/database layer
- editor selections must align with stable anchor and selector rules

## Needs design or grounding before promotion

- exact schema boundary between ProseMirror documents and canonical structures
- selection/anchor mapping rules
- collaborative/editor plugin assumptions, if any
- fixture corpus for edit stability and render fidelity

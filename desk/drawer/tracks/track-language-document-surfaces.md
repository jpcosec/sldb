---
id: track-language-document-surfaces
status: proposed
summary: Bundle surface-expansion work across Lisp, Markdown successors, anchors, identity, and additional document families.
tags:
- workspace:desk
- artifact:track
- system:sldb
history:
- "2026-07-29: drafted as interstitial planning layer between features and promotable tasks."
references:
- also_core.md
- interfaces.md
- plan_core.md
items:
- desk/drawer/features/feature-anchoring-and-selector-stability.md
- desk/drawer/features/feature-node-identity-and-reconciliation.md
- desk/drawer/features/feature-lisp-surface-expansion.md
- desk/drawer/features/feature-multi-family-document-support.md
- desk/drawer/features/feature-renderers-and-materializers-beyond-markdown.md
- desk/drawer/features/feature-treesitter-code-family-support.md
- desk/drawer/features/feature-prosemirror-editor-surface.md
---

# Language and document surfaces track

## Goal

Group the expansion work for authored/document surfaces and their canonicalization/materialization contracts.

## Promotion order inside the track

1. Anchoring and selector stability
2. Node identity and reconciliation
3. Lisp surface expansion
4. Tree-sitter code family support
5. ProseMirror editor surface
6. Multi-family document support
7. Renderers and materializers beyond Markdown

## Needs design or grounding before promotion

- how code/editor surfaces depend on anchoring and identity rules
- family rollout order after Markdown
- shared vs surface-specific canonicalization constraints
